#!/usr/bin/env python3
"""
build_manual.py -- docs/manual/*.md -> data/manual.js

The transcribed 732A manual ships inside the page. This turns every markdown
file under docs/manual/ (README.md excepted: it documents the transcription,
it is not the manual) into one generated script that calls
BoardExplorer.registerManual({ source, generated, sections: [...] }).

A section starts at every ##/###/#### heading. Text that precedes the first
such heading in a file (the file's "Section N" title and its source line)
becomes a title-page section of its own so nothing transcribed is dropped.

Each section carries:
  id        slug of the heading, unique across the manual
  title     the heading with its number and page parenthetical removed
  section   the manual's own number parsed off the heading -- '3-10',
            'Table 4-3', 'Figure 8-1', 'Errata #12', 'Change #2', 'Section 7A'
            -- or null
  pages     {text, pdf: [n, ...], manual: ['4-9', ...]} from the
            "(PDF pNN, manual pX-Y)" parenthetical; a sub-heading without
            one gets its parent's, flagged inherited: true; else null
  file      the source file name
  group     the table-of-contents heading this file belongs under
  level     2, 3 or 4
  boards    the assemblies the heading names, else the one the nearest
            ancestor heading names, else [] -- the context bare
            designators resolve in
  html      the body rendered from markdown at build time
  text      the body as plain text, for search
  mentions  [{ref, assembly}] -- every designator the section names, once

Markdown is converted here rather than at runtime: headings, paragraphs
(line breaks kept, since the transcription is line-oriented), **bold**,
*italic*, pipe tables, ordered and unordered lists, blockquotes, code spans
and horizontal rules. Source text is HTML-escaped. Standard library only.

Mentions: a designator with an explicit assembly prefix (A4Q12, "A3 P3")
belongs to that assembly. Otherwise the assembly comes from the section's own
heading (a heading naming two, "(A3 and A4)", gives one mention per
assembly), else from the nearest ancestor heading when that names exactly
one, else from CONTEXT_OVERRIDES (the two sections whose text names a board
for another reason), else from an errata "Rev.-C, A4 Regulator PCB Assembly"
line that opened the section, else from the same paragraph when it names
exactly one of A1..A7, else null -- shown by the page as "names Q1 without saying which
board". A wrong resolution sends someone to the wrong board, so ambiguity
resolves to null, never to a guess.

Usage: tools/build_manual.py            # writes data/manual.js
"""
import html
import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'docs', 'manual')
OUT = os.path.join(ROOT, 'data', 'manual.js')

# The manual's own order, which the file names do not quite give: sorted by
# name, 04-calibration lands ahead of 04-maintenance although its paragraphs
# (4-32..) follow maintenance's (4-1..4-31). Files not listed here follow, in
# name order, under a group named after their first heading.
FILES = [
    ('01-specifications.md',                 'Section 1 · Specifications'),
    ('02-operation.md',                      'Section 2 · Operation'),
    ('03-theory.md',                         'Section 3 · Theory of operation'),
    ('04-maintenance.md',                    'Section 4 · Maintenance'),
    ('04-calibration.md',                    'Section 4 · Calibration'),
    ('04-service-troubleshooting.md',        'Section 4 · Service and troubleshooting'),
    ('05-parts-final-assembly.md',           'Section 5 · Parts, final assembly'),
    ('05-parts-a1-a2.md',                    'Section 5 · Parts, A1 and A2'),
    ('05-parts-a6-a7.md',                    'Section 5 · Parts, A5 figure, A6 and A7'),
    ('06-07-accessories-general.md',         'Sections 6, 7, 7A · Accessories, general information'),
    ('07-abbreviations.md',                  'Section 7 · Abbreviations'),
    ('07-manufacturer-codes.md',             'Section 7 · Manufacturer codes'),
    ('08-schematic-and-interconnect-notes.md', 'Section 8 · Schematic notes'),
    ('errata-issue3-1985.md',                'Errata · Issue 3, 7/85'),
]
SKIP = {'README.md'}

# Designator families that occur in the manual's text. LM (LM301, an IC part
# number) and the stock-number shapes (M07-200-603, 732A-1301, 1N5240) are
# kept out by the family list and the boundaries.
FAMILIES = r'CR|VR|RT|RV|TP|DS|HR|BT|MP|XF|FL|[QRCUFWSEJPKLTH]'
DESIGNATOR = re.compile(
    r'(?<![A-Za-z0-9])(?:A(\d+)\s?)?(' + FAMILIES + r')(\d+)(?![A-Za-z0-9])')
# An assembly named on its own -- "located on A4", "(A3 and A4)" -- rather
# than as a designator's prefix.
ASSEMBLY = re.compile(r'(?<![A-Za-z0-9])A([1-7])(?![0-9A-Za-z])')
REV_LINE = re.compile(r'^Rev\.?\s*-?\s*[A-Z]?\b')

# Sections whose bare designators the text itself would send to the wrong
# board, by section number -> the board the whole section is about. The
# paragraph rule takes the one assembly a paragraph names, and these
# paragraphs name a board for another reason: 4-44 (Battery Charger
# Adjustment, an A3 procedure) says W1 and CR27 are "on A2" in two steps and
# on the A3 AC Module in another, and Figure 8-3 draws both on A3; 4-53 (Oven
# Repair) names U1, U2, Q1, Q2, Q5 and TP11-TP14 of the A5 reference circuit
# in a sentence whose only board is the A7 jumper PCB. An explicit prefix
# (A4Q12) in these sections still wins.
CONTEXT_OVERRIDES = {
    '4-44': 'A3',
    '4-53': 'A5',
}

PDF_PAGES = re.compile(r'PDF\s+p(?:ages?\s*)?(\d+)(?:\s*[-–]\s*(\d+))?')
MANUAL_PAGES = re.compile(r'manual\s+p(?:ages?\s*)?([^)]*)')
PAGE_TOKEN = re.compile(r'\d+[A-Z]?-\d+')
PAREN = re.compile(r'\(([^()]*)\)')

# --------------------------------------------------------------------------
# headings


def parse_heading(raw):
    """-> (title, section, pages) from a heading's text."""
    text = raw.strip()
    pages = None
    # The page parenthetical: "(PDF p21, manual p3-1)", or the "PDF p32,
    # manual p4-8" tail inside a longer parenthetical.
    for m in PAREN.finditer(text):
        inner = m.group(1)
        if 'PDF p' not in inner:
            continue
        pm = PDF_PAGES.search(inner)
        if not pm:
            continue
        pdf = [int(pm.group(1))]
        if pm.group(2):
            pdf = list(range(pdf[0], int(pm.group(2)) + 1))
        mm = MANUAL_PAGES.search(inner)
        manual = PAGE_TOKEN.findall(mm.group(1)) if mm else []
        page_text = re.sub(r'^Source:\s*', '', inner).strip()
        if re.match(r'^(Source:\s*)?PDF p', inner):
            text = (text[:m.start()] + text[m.end():]).strip()
        else:
            # "(continued from preceding page — ..., PDF p32, manual p4-8)"
            cut = re.sub(r',?\s*PDF p[^,)]*(?:,\s*manual p[^)]*)?', '', inner).strip()
            text = text[:m.start()] + '(' + cut + ')' + text[m.end():]
            page_text = inner[inner.index('PDF p'):].strip()
        pages = {'text': page_text, 'pdf': pdf, 'manual': manual}
        break
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[—–·-]\s*', '', text)

    section = None
    m = re.match(r'^(Table|Figure)\s+(\d+[A-Z]?-\d+)(\s*\(cont\))?\s*[.:]?\s*', text)
    if m:
        section = m.group(1) + ' ' + m.group(2)
        text = text[m.end():] + (' (cont)' if m.group(3) else '')
    else:
        m = re.match(r'^(\d+[A-Z]?-\d+[A-Za-z]?)\.\s*', text)
        if m:
            section = m.group(1)
            text = text[m.end():]
        else:
            m = re.match(r'^(ERRATA|CHANGE)\s+#(\d+)\s*(?:-\s*(.*))?$', text)
            if m:
                section = m.group(1).capitalize() + ' #' + m.group(2)
                text = section + (' (' + m.group(3).strip() + ')' if m.group(3) else '')
            else:
                m = re.match(r'^Section\s+(\d+[A-Z]?)\b[\s.:—–-]*', text)
                if m:
                    section = 'Section ' + m.group(1)
                    text = text[m.end():]
    # Errata page headings: '— footer "6/84", page "-2-"'.
    m = re.match(r'^footer\s+"([^"]+)",\s*page\s+"([^"]+)"$', text)
    if m:
        text = 'Errata page ' + m.group(2) + ' (' + m.group(1) + ')'
    title = text.strip() or section or raw.strip()
    return title, section, pages


def slugify(s):
    s = re.sub(r'\(PDF[^)]*\)', '', s)
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s[:64].rstrip('-') or 'section'


# --------------------------------------------------------------------------
# markdown -> blocks -> html

INLINE_CODE = re.compile(r'`([^`\n]+)`')
BOLD = re.compile(r'\*\*(?=\S)(.+?)(?<=\S)\*\*')
ITALIC = re.compile(r'(?<![*\w])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![*\w])')


def inline(text):
    """Escaped HTML with the inline marks applied."""
    out = []
    pos = 0
    # Code spans first, so nothing inside them is formatted.
    for m in INLINE_CODE.finditer(text):
        out.append(marks(text[pos:m.start()]))
        out.append('<code>' + html.escape(m.group(1), quote=False) + '</code>')
        pos = m.end()
    out.append(marks(text[pos:]))
    return ''.join(out)


# The one HTML tag the transcription uses: a line break inside a table cell,
# which pipe tables have no markdown for. Everything else in the source is
# escaped and shown as typed.
BR = re.compile(r'<br\s*/?>', re.I)
ESCAPED_BR = re.compile(r'&lt;br\s*/?&gt;', re.I)


def marks(text):
    s = html.escape(text, quote=False)
    s = ESCAPED_BR.sub('<br>', s)
    s = BOLD.sub(r'<strong>\1</strong>', s)
    s = ITALIC.sub(r'<em>\1</em>', s)
    return s


def strip_inline(text):
    s = BR.sub(' ', text)
    s = INLINE_CODE.sub(r'\1', s)
    s = BOLD.sub(r'\1', s)
    s = ITALIC.sub(r'\1', s)
    return s


def is_table_sep(line):
    return re.match(r'^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$', line) is not None


def split_row(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]


LIST_ITEM = re.compile(r'^(\s*)(?:([-*])|(\d+)\.)\s+(.*)$')


def parse_blocks(lines):
    """Lines of one section -> [{type, ...}]. Types: p, h1, table, list,
    quote, hr. Each block also carries 'text', its plain text."""
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if re.match(r'^\s*---+\s*$', line):
            blocks.append({'type': 'hr', 'text': ''})
            i += 1
            continue
        m = re.match(r'^#\s+(.*)$', line)
        if m:
            blocks.append({'type': 'h1', 'text': m.group(1).strip()})
            i += 1
            continue
        if line.lstrip().startswith('>'):
            quote = []
            while i < n and lines[i].lstrip().startswith('>'):
                quote.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            blocks.append({'type': 'quote', 'lines': quote, 'text': ' '.join(quote)})
            continue
        if '|' in line and i + 1 < n and is_table_sep(lines[i + 1]):
            head = split_row(line)
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            # Every row is a paragraph of its own for mention resolution: a
            # row of Table 4-3 names its board in the first cell.
            for r in rows:
                blocks.append({'type': 'row', 'cells': r, 'text': ' '.join(r)})
            blocks.append({'type': 'table-end', 'head': head, 'nrows': len(rows), 'text': ''})
            continue
        m = LIST_ITEM.match(line)
        if m:
            items = []
            while i < n:
                mm = LIST_ITEM.match(lines[i])
                if not mm:
                    break
                indent = len(mm.group(1).replace('\t', '    '))
                items.append({'indent': indent, 'ordered': mm.group(3) is not None,
                              'n': int(mm.group(3)) if mm.group(3) else None,
                              'text': mm.group(4).strip()})
                i += 1
                # Continuation lines: indented text that is not a new item.
                while i < n and lines[i].strip() and not LIST_ITEM.match(lines[i]) \
                        and lines[i].startswith((' ', '\t')) and not lines[i].lstrip().startswith(('#', '|', '>')):
                    items[-1]['text'] += ' ' + lines[i].strip()
                    i += 1
                # The procedures put a blank line between steps. A blank line
                # followed by another item continues the list; anything else
                # ends it.
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and j > i and LIST_ITEM.match(lines[j]):
                    i = j
            for it in items:
                blocks.append({'type': 'item', 'item': it, 'text': it['text']})
            blocks.append({'type': 'list-end', 'text': ''})
            continue
        para = []
        while i < n and lines[i].strip() and not re.match(r'^\s*---+\s*$', lines[i]) \
                and not lines[i].startswith('#') and not lines[i].lstrip().startswith('>') \
                and not LIST_ITEM.match(lines[i]) \
                and not ('|' in lines[i] and i + 1 < n and is_table_sep(lines[i + 1])):
            para.append(lines[i].strip())
            i += 1
        blocks.append({'type': 'p', 'lines': para, 'text': ' '.join(para)})
    return blocks


def render_blocks(blocks):
    out = []
    pending_rows = []
    pending_items = []
    for b in blocks:
        t = b['type']
        if t == 'row':
            pending_rows.append(b['cells'])
            continue
        if t == 'table-end':
            out.append(render_table(b['head'], pending_rows))
            pending_rows = []
            continue
        if t == 'item':
            pending_items.append(b['item'])
            continue
        if t == 'list-end':
            out.append(render_list(pending_items))
            pending_items = []
            continue
        if t == 'hr':
            out.append('<hr>')
        elif t == 'h1':
            out.append('<h4>' + inline(b['text']) + '</h4>')
        elif t == 'quote':
            out.append('<blockquote>' + '<br>'.join(inline(l) for l in b['lines']) + '</blockquote>')
        elif t == 'p':
            out.append('<p>' + '<br>'.join(inline(l) for l in b['lines']) + '</p>')
    # A rule between sections in the source ends up at the edge of one of
    # them, where it draws a line under nothing.
    while out and out[0] == '<hr>':
        out.pop(0)
    while out and out[-1] == '<hr>':
        out.pop()
    return '\n'.join(out)


def render_table(head, rows):
    ncol = max([len(head)] + [len(r) for r in rows])
    h = '<div class="manual-table"><table><thead><tr>'
    for c in range(ncol):
        h += '<th>' + (inline(head[c]) if c < len(head) else '') + '</th>'
    h += '</tr></thead><tbody>'
    for r in rows:
        h += '<tr>'
        for c in range(ncol):
            h += '<td>' + (inline(r[c]) if c < len(r) else '') + '</td>'
        h += '</tr>'
    return h + '</tbody></table></div>'


def render_list(items):
    """Nested by indentation; each run of items opens <ol start=N> or <ul>."""
    out = []
    stack = []   # [(indent, tag)]

    def close_to(indent):
        while stack and stack[-1][0] > indent:
            out.append('</li></' + stack.pop()[1] + '>')

    for it in items:
        tag = 'ol' if it['ordered'] else 'ul'
        if stack and it['indent'] > stack[-1][0]:
            start = ' start="%d"' % it['n'] if it['ordered'] and it['n'] not in (None, 1) else ''
            out.append('<' + tag + start + '><li>' + inline(it['text']))
            stack.append((it['indent'], tag))
            continue
        close_to(it['indent'])
        if stack and stack[-1][0] == it['indent'] and stack[-1][1] == tag:
            out.append('</li><li>' + inline(it['text']))
            continue
        if stack and stack[-1][0] == it['indent']:
            out.append('</li></' + stack.pop()[1] + '>')
        start = ' start="%d"' % it['n'] if it['ordered'] and it['n'] not in (None, 1) else ''
        out.append('<' + tag + start + '><li>' + inline(it['text']))
        stack.append((it['indent'], tag))
    while stack:
        out.append('</li></' + stack.pop()[1] + '>')
    return ''.join(out)


def plain_text(blocks):
    parts = []
    for b in blocks:
        if b['text']:
            parts.append(strip_inline(b['text']))
    return re.sub(r'\s+', ' ', ' '.join(parts)).strip()


# --------------------------------------------------------------------------
# mentions


def assemblies_named(text):
    return sorted(set('A' + m.group(1) for m in ASSEMBLY.finditer(text)))


def mentions_for(heading_text, ancestor_context, blocks, override=None):
    heading_asms = assemblies_named(heading_text)
    section_context = override
    seen = set()
    out = []

    def add(ref, asm):
        key = (ref, asm)
        if key in seen:
            return
        seen.add(key)
        out.append({'ref': ref, 'assembly': asm})

    def scan(text, para_context):
        for m in DESIGNATOR.finditer(strip_inline(text)):
            ref = m.group(2) + m.group(3)
            if m.group(1):
                add(ref, 'A' + m.group(1))
                continue
            if heading_asms:
                for a in heading_asms:
                    add(ref, a)
            elif ancestor_context:
                add(ref, ancestor_context)
            elif section_context:
                add(ref, section_context)
            else:
                add(ref, para_context)

    scan(heading_text, None)
    for b in blocks:
        if not b['text']:
            continue
        named = assemblies_named(b['text'])
        if REV_LINE.match(b['text']) and len(named) == 1:
            section_context = named[0]
        scan(b['text'], named[0] if len(named) == 1 else None)
    # A ref the section places on a board in one paragraph and names bare in
    # the next is the same part: the bare mention would only add an
    # "unresolved" line under a resolved one on the same card.
    resolved = set(m['ref'] for m in out if m['assembly'])
    return [m for m in out if m['assembly'] or m['ref'] not in resolved]


# --------------------------------------------------------------------------
# files -> sections

HEADING = re.compile(r'^(#{2,4})\s+(.*?)\s*$')


def build_file(name, group):
    with open(os.path.join(SRC, name), encoding='utf-8') as f:
        lines = f.read().split('\n')

    # (level, heading_text, body_lines)
    chunks = []
    current = (0, None, [])
    for line in lines:
        m = HEADING.match(line)
        if m:
            chunks.append(current)
            current = (len(m.group(1)), m.group(2), [])
        else:
            current[2].append(line)
    chunks.append(current)

    sections = []
    ancestors = {}   # level -> assemblies named by the last heading at that level
    anc_pages = {}   # level -> pages of the last heading at that level
    for level, heading, body in chunks:
        blocks = parse_blocks(body)
        if level == 0:
            # The file's preamble: its "# Section N" title(s) and source line.
            h1 = [b['text'] for b in blocks if b['type'] == 'h1']
            rest = [b for b in blocks if b['type'] != 'h1']
            if not plain_text(rest):
                continue
            heading = ' — '.join(h1) if h1 else group
            blocks = rest
            level = 1
        title, section, pages = parse_heading(heading)
        # A sub-heading with no page parenthetical of its own (the Section 8
        # legends under one figure heading) is on its parent's page: carry
        # that down, flagged, so every heading in the reader has a page.
        if pages is None:
            for lv in range(level - 1, 0, -1):
                if anc_pages.get(lv):
                    pages = dict(anc_pages[lv], inherited=True)
                    break
        anc_pages[level] = pages
        named = assemblies_named(heading)
        ancestors[level] = named
        for deeper in list(ancestors):
            if deeper > level:
                del ancestors[deeper]
                anc_pages.pop(deeper, None)
        ancestor_context = None
        for lv in range(level - 1, 0, -1):
            if lv in ancestors:
                if len(ancestors[lv]) == 1:
                    ancestor_context = ancestors[lv][0]
                break
        sections.append({
            'id': slugify(heading),
            'title': title,
            'section': section,
            'pages': pages,
            'file': name,
            'group': group,
            'level': level,
            # The boards the section is about, as its heading (or the nearest
            # ancestor heading naming one) says: the context bare designators
            # resolve in, kept so the reader links them by the same rule.
            'boards': named or ([ancestor_context] if ancestor_context else
                                ([CONTEXT_OVERRIDES[section]] if section in CONTEXT_OVERRIDES else [])),
            'html': render_blocks(blocks),
            'text': plain_text(blocks),
            'mentions': mentions_for(heading, ancestor_context, blocks,
                                     CONTEXT_OVERRIDES.get(section)),
        })
    return sections


def main():
    names = sorted(n for n in os.listdir(SRC) if n.endswith('.md') and n not in SKIP)
    order = {name: i for i, (name, _) in enumerate(FILES)}
    groups = dict(FILES)
    names.sort(key=lambda n: (order.get(n, len(FILES)), n))

    sections = []
    for name in names:
        group = groups.get(name)
        if not group:
            with open(os.path.join(SRC, name), encoding='utf-8') as f:
                first = next((l for l in f if l.startswith('#')), name)
            group = re.sub(r'^#+\s*', '', first).strip() or name
        sections.extend(build_file(name, group))

    # Unique ids: four "NOTES (verbatim)" headings would otherwise collide.
    seen = {}
    for s in sections:
        base = s['id']
        if base in seen:
            seen[base] += 1
            s['id'] = base + '-' + str(seen[base])
        else:
            seen[base] = 1

    data = {
        'source': 'Fluke 732A Instruction Manual, P/N 645051, May 1983, with Change/Errata Issue 3 (7/85); transcribed in docs/manual/',
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'files': names,
        'sections': sections,
    }
    body = json.dumps(data, ensure_ascii=False, indent=1)
    # Harmless in an external script, but the file must never be able to end
    # an inline <script> if someone pastes it into one.
    body = body.replace('</', '<\\/')
    header = (
        '/*\n'
        ' * data/manual.js -- GENERATED by tools/build_manual.py. Do not edit.\n'
        ' *\n'
        ' * The 732A manual as sections, built from docs/manual/:\n' +
        ''.join(' *   %s\n' % n for n in names) +
        ' *\n'
        ' * Rebuild: tools/build_manual.py\n'
        ' */\n'
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(header + 'BoardExplorer.registerManual(' + body + ');\n')

    numbered = sum(1 for s in sections if s['section'])
    mentions = sum(len(s['mentions']) for s in sections)
    unresolved = sum(1 for s in sections for m in s['mentions'] if m['assembly'] is None)
    print('%s: %d sections from %d files, %d with a section number, %d mentions (%d unresolved), %d KB'
          % (os.path.relpath(OUT, ROOT), len(sections), len(names), numbered, mentions,
             unresolved, os.path.getsize(OUT) // 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main())
