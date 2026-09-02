# Manual tab — brief (engine phase 2)

Read the spec addendum "the manual inside the tool" in
`docs/superpowers/specs/2026-09-01-732a-atlas-design.md` and the engine
conventions in the reference `CLAUDE.md`. Files: `tools/build_manual.py` (new),
`js/manual.js` (new), `js/search.js`, `js/app.js`, `index.html`, `css/app.css`.

## `tools/build_manual.py`

- Input: every `docs/manual/*.md` in name order (01-specifications …
  errata-issue3-1985). Output: `data/manual.js` containing
  `BoardExplorer.registerManual({ source, generated, sections: [...] })`.
- A section starts at every `##`/`###`/`####` heading. Fields: `id` (slug of
  the heading), `title`, `section` (the manual's paragraph/table/figure number
  parsed off the heading, e.g. `3-10`, `Table 4-3`, `Figure 8-1`, `Errata #12`),
  `pages` (the "(PDF pNN, manual pX-Y)" parenthetical, kept as text and as
  numbers), `file`, `html`, `text` (plain, for search), `mentions`.
- Markdown → HTML: headings, paragraphs, `**bold**`, `*italic*`, tables
  (pipe rows with a `---` separator), ordered and unordered lists, blockquote,
  code spans, horizontal rules. Escape HTML in source text. No external
  library; Python 3.9 standard library only.
- `mentions`: every designator token in the section's text (`A4Q12`, `Q1`,
  `CR27`, `TP5`, `R20`, `U2`, `RT1`, `DS1`, `F2`, `W1`, `S1`, `HR1`, `BT1`,
  `E33`, `J10`, `P3`) as `{ ref, assembly }` where `assembly` is taken from an
  explicit prefix (`A4Q12` → A4, Q12), else from the heading or the same
  paragraph naming exactly one of A1…A7 ("(A3 and A4)" gives two: emit one
  mention per assembly), else `null`. Deduplicate per section.
- The header comment names the source files and says the file is generated.

## `js/manual.js`

- An ES5 IIFE hanging `window.Manual` off the global; `BoardExplorer.
  registerManual(data)` stores the sections (add the method in `registry.js`
  — one line, plus `BoardExplorer.manual()` to read it back).
- `Manual.render(panelBody, opts)`: left, the table of contents grouped by
  file (Section 1, 2, 3, 4, 5, 6/7, 7A, 8 notes, Errata) with the section
  numbers; right, the current section's HTML with its page reference under
  the heading and prev/next links. `opts.section` opens one; `opts.query`
  highlights every occurrence with `<mark>` and scrolls to the first.
- `Manual.search(query)`: case-insensitive substring over `text`, returns
  `[{ section, snippet }]` with a ~120-character snippet around the first hit,
  at most 30 results, ranked: section-number match first, title match, then
  body.
- `Manual.mentions(ref, assemblyId)`: sections whose `mentions` include
  `{ref}` with `assembly === assemblyId` or `assembly === null`, each flagged
  `resolved: true|false`.
- Storage key `fluke732a.manual.last.v1` remembers the last section opened
  (per browser, not per unit).

## Wiring (`app.js`, `index.html`, `css/app.css`, `search.js`)

- Mode button `<button data-mode="manual"><u>M</u>anual</button>` after
  Symptoms; key `M`; the stage keeps showing the board (the manual is read in
  the panel, the board stays visible for the part it talks about). When the
  panel is in manual mode, the detail dock stays usable.
- Global search: after the part hits, a "In the manual" group with up to 8
  `Manual.search()` results; choosing one sets mode `manual` and opens the
  section with the query highlighted. Keep the existing hit types untouched.
- Part / test point card: a section **In the manual** listing
  `Manual.mentions(ref, assembly.id)` as links (`§3-11 Power Supplies (A3 and
  A4)`), unresolved ones suffixed "· names Q1 without saying which board";
  clicking opens the section in the panel with the designator highlighted.
  Hide the section when there are no mentions.
- Follower windows (linked view) ignore manual mode as they ignore the other
  panel modes.
- `index.html` loads `js/manual.js` before `js/app.js` and `data/manual.js`
  with the datasets. `tools/make_release.sh` picks it up automatically because
  it is named in `index.html`.
- CSS: the reader uses the panel's existing type scale; tables scroll
  horizontally inside the panel; `<mark>` uses the amber highlight already
  defined for search hits.

## Proof

`node --check` all files; build `data/manual.js` from the real
`docs/manual/`; load it in node with the vm recipe and print the section
count, the number of sections with a `section` number, the mentions for
`A3`/`Q1` and `A5`/`U2`; run `Manual.search('CR27')` and show the snippet
comes from §4-44.
