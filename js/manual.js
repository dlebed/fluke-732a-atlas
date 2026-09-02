/*
 * manual.js — the transcribed 732A manual inside the page: a table of
 * contents, a section reader, search over the text, and the "In the manual"
 * mentions a part's card lists.
 *
 * The sections arrive through BoardExplorer.registerManual(), called by the
 * generated data/manual.js at load time; nothing is fetched. The markdown was
 * converted by tools/build_manual.py when that file was built, so this file
 * only lays out HTML it is handed, searches plain text, and links the
 * designators in it to the board that is open. It knows nothing about any
 * particular board: with no dataset loaded the reader still works, it just
 * has nothing to link to.
 */
(function (global) {
  'use strict';

  var BE = global.BoardExplorer;
  var LAST_KEY = 'fluke732a.manual.last.v1';   // per browser, not per unit

  var Manual = {};

  // Filled in by app.js: what a designator in the text does when clicked or
  // hovered. Left null, designators stay plain text.
  Manual.hooks = { select: null, hover: null };

  /* ================= data ================= */

  var index = null;   // built once per registered manual

  function ensureIndex() {
    var d = BE && BE.manual ? BE.manual() : null;
    if (!d) { index = null; return null; }
    if (index && index.source === d) return index;
    var byId = {}, groups = [], groupByName = {};
    (d.sections || []).forEach(function (s, i) {
      s.index = i;
      byId[s.id] = s;
      var g = groupByName[s.group];
      if (!g) {
        g = groupByName[s.group] = { name: s.group, sections: [] };
        groups.push(g);
      }
      g.sections.push(s);
    });
    index = { source: d, list: d.sections || [], byId: byId, groups: groups };
    return index;
  }

  Manual.sections = function () {
    var ix = ensureIndex();
    return ix ? ix.list : [];
  };

  Manual.get = function (id) {
    var ix = ensureIndex();
    return (ix && ix.byId[id]) || null;
  };

  Manual.loaded = function () { return Manual.sections().length > 0; };

  /** '§3-10', 'Table 4-3', 'Errata #12'; '' when the section has no number. */
  Manual.label = function (s) {
    if (!s || !s.section) return '';
    return /^\d/.test(s.section) ? '§' + s.section : s.section;
  };

  /* ================= search ================= */

  /**
   * Case-insensitive substring search over the manual.
   *
   * Ranked: a section-number match first (typing "4-44" wants §4-44, not
   * every paragraph that cites it), then a title match, then the body.
   * @returns [{section, snippet, where, score}], at most `limit` (30).
   */
  Manual.search = function (query, limit) {
    var q = String(query || '').trim().toLowerCase();
    if (!q) return [];
    var qn = q.replace(/^§\s*/, '');
    var numeric = /\d/.test(qn);
    var out = [];
    Manual.sections().forEach(function (s) {
      var num = (s.section || '').toLowerCase();
      var bare = num.replace(/^(table|figure|section|errata|change)\s+#?/, '');
      var title = (s.title || '').toLowerCase();
      var text = (s.text || '').toLowerCase();
      var score = 0, where = null, at = -1;
      if (num && (num === qn || bare === qn)) { score = 3; where = 'number'; }
      else if (num && numeric && (num.indexOf(qn) === 0 || bare.indexOf(qn) === 0)) { score = 2.5; where = 'number'; }
      else if (title.indexOf(q) >= 0) { score = 2; where = 'title'; }
      else if ((at = text.indexOf(q)) >= 0) { score = 1; where = 'body'; }
      if (!score) return;
      if (at < 0) at = text.indexOf(q);
      out.push({ section: s, score: score, where: where, snippet: snippetFor(s.text || '', at) });
    });
    out.sort(function (a, b) {
      return b.score - a.score || a.section.index - b.section.index;
    });
    return out.slice(0, limit || 30);
  };

  /** ~120 characters around `at`, cut at word boundaries; the opening of the
   *  section when the match was in its number or title. */
  function snippetFor(text, at) {
    if (!text) return '';
    var start = at > 50 ? at - 50 : 0;
    var end = Math.min(text.length, start + 120);
    if (start > 0) {
      var sp = text.indexOf(' ', start);
      if (sp >= 0 && sp < start + 20) start = sp + 1;
    }
    if (end < text.length) {
      var sp2 = text.lastIndexOf(' ', end);
      if (sp2 > end - 20) end = sp2;
    }
    return (start > 0 ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }

  /* ================= mentions ================= */

  /**
   * The sections that name a designator: those whose mention carries this
   * assembly, and those whose mention names no board at all -- the manual
   * says "Q1" and could mean any board's Q1, so it shows on every board that
   * has one, flagged `resolved: false`.
   */
  Manual.mentions = function (ref, assemblyId) {
    var R = String(ref || '').toUpperCase();
    if (!R) return [];
    var out = [];
    Manual.sections().forEach(function (s) {
      var hit = null;
      (s.mentions || []).forEach(function (m) {
        if (String(m.ref).toUpperCase() !== R) return;
        if (m.assembly === assemblyId) hit = { section: s, resolved: true };
        else if (m.assembly === null && !hit) hit = { section: s, resolved: false };
      });
      if (hit) out.push(hit);
    });
    return out;
  };

  /* ================= reader ================= */

  var view = {
    host: null, root: null,
    sectionId: null, query: '', filter: '',
    asmId: null,        // the board the reader's designator links point at
    tocHidden: false
  };

  function currentAsmId() {
    var asm = BE && BE.state ? BE.state.assembly : null;
    return asm ? asm.id : null;
  }

  function remembered(ix) {
    try {
      var id = global.localStorage.getItem(LAST_KEY);
      return id && ix.byId[id] ? id : null;
    } catch (err) { return null; }
  }

  function remember(id) {
    try { global.localStorage.setItem(LAST_KEY, id); } catch (err) { /* session only */ }
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /**
   * Lay the manual out in `host`: contents on the left, the open section on
   * the right.
   *
   * @param opts.section  id to open (defaults to the last one opened)
   * @param opts.query    highlight every occurrence and scroll to the first
   * @param opts.filter   a search term: the contents column shows the
   *                      sections matching it instead of the full list
   *
   * Called on every panel refresh, so it rebuilds only what changed: a
   * reading recorded on the board must not scroll the page being read.
   */
  Manual.render = function (host, opts) {
    var o = opts || {};
    var ix = ensureIndex();
    if (!ix || !ix.list.length) {
      host.innerHTML = '<div class="empty"><strong>The manual is not loaded</strong>' +
        'data/manual.js is missing — build it with tools/build_manual.py.</div>';
      view.root = null;
      return;
    }
    var id = o.section && ix.byId[o.section] ? o.section
      : (view.sectionId && ix.byId[view.sectionId] ? view.sectionId
        : (remembered(ix) || ix.list[0].id));
    var query = o.section ? String(o.query || '') : view.query;
    var filter = o.filter == null ? view.filter : String(o.filter).trim();

    var attached = view.root && view.root.parentNode === host && view.host === host;
    // A section asked for by name is re-rendered even when it is already
    // open: the point of the click was to land on the highlighted term again.
    // A board change re-renders too, since the designator links in the text
    // belong to the board that was open when they were made.
    var asmId = currentAsmId();
    var sectionChanged = !!o.section || id !== view.sectionId || query !== view.query ||
      asmId !== view.asmId;
    var filterChanged = filter !== view.filter;
    view.sectionId = id;
    view.query = query;
    view.filter = filter;
    view.asmId = asmId;
    view.host = host;

    if (!attached) {
      host.innerHTML = '';
      view.root = document.createElement('div');
      view.root.className = 'manual' + (view.tocHidden ? ' is-toc-hidden' : '');
      view.root.appendChild(document.createElement('nav')).className = 'manual-toc';
      view.root.appendChild(document.createElement('article')).className = 'manual-reader';
      host.appendChild(view.root);
      wire(view.root);
      renderToc();
      renderReader();
    } else {
      if (filterChanged) renderToc();
      if (sectionChanged) { renderReader(); markCurrent(); }
    }
    remember(id);
  };

  /** Open a section from inside the reader. */
  function open(id, query) {
    view.sectionId = id;
    view.query = query || '';
    remember(id);
    renderReader();
    markCurrent();
  }

  function renderToc() {
    var ix = ensureIndex();
    var nav = view.root.querySelector('.manual-toc');
    var html = '';
    if (view.filter) {
      var hits = Manual.search(view.filter);
      html += '<div class="manual-group"><header>Results <span class="count">' +
        hits.length + '</span></header>';
      if (!hits.length) {
        html += '<div class="manual-none">Nothing in the manual matches “' +
          esc(view.filter) + '”.</div>';
      } else {
        html += '<ul>' + hits.map(function (h) {
          var s = h.section;
          return '<li data-section="' + esc(s.id) + '" data-query="' + esc(view.filter) +
            '" tabindex="0" class="hit' + (s.id === view.sectionId ? ' is-current' : '') + '">' +
            '<span class="row"><span class="num">' + esc(Manual.label(s)) + '</span>' +
            '<span class="ttl">' + esc(s.title) + '</span></span>' +
            (h.snippet ? '<span class="snip">' + esc(h.snippet) + '</span>' : '') +
            '</li>';
        }).join('') + '</ul>';
      }
      html += '</div>';
    } else {
      html += ix.groups.map(function (g) {
        return '<div class="manual-group"><header>' + esc(g.name) + '</header><ul>' +
          g.sections.map(function (s) {
            return '<li data-section="' + esc(s.id) + '" tabindex="0" class="lv' + s.level +
              (s.id === view.sectionId ? ' is-current' : '') + '">' +
              (s.section ? '<span class="num">' + esc(Manual.label(s)) + '</span>' : '') +
              '<span class="ttl" title="' + esc(s.title) + '">' + esc(s.title) + '</span></li>';
          }).join('') + '</ul></div>';
      }).join('');
    }
    nav.innerHTML = html;
    if (view.filter) markText(nav, view.filter);
    markCurrent();
  }

  function markCurrent() {
    var nav = view.root.querySelector('.manual-toc');
    var current = null;
    Array.prototype.forEach.call(nav.querySelectorAll('li[data-section]'), function (li) {
      var on = li.dataset.section === view.sectionId;
      li.classList.toggle('is-current', on);
      if (on && !current) current = li;
    });
    if (current) revealIn(nav, current, false);
  }

  /**
   * Scroll `container` so `el` shows, and only `container`: scrollIntoView
   * would also nudge every scrollable ancestor, the page included, and the
   * contents column keeps its group heading stuck at the top, which the
   * 'nearest' alignment does not know to clear.
   */
  function revealIn(container, el, center) {
    var cr = container.getBoundingClientRect(), er = el.getBoundingClientRect();
    var top = er.top - cr.top + container.scrollTop;
    var pad = 44;   // the sticky heading above the rows
    if (center) {
      container.scrollTop = Math.max(0, top - (container.clientHeight - er.height) / 2);
    } else if (er.top - cr.top < pad) {
      container.scrollTop = Math.max(0, top - pad);
    } else if (er.bottom > cr.bottom) {
      container.scrollTop = top - container.clientHeight + er.height + 8;
    }
  }

  function short(s) {
    var label = Manual.label(s);
    if (label) return label;
    var t = s.title || '';
    return t.length > 22 ? t.slice(0, 21) + '…' : t;
  }

  function navHTML(s, ix, bottom) {
    var prev = s.index > 0 ? ix.list[s.index - 1] : null;
    var next = s.index + 1 < ix.list.length ? ix.list[s.index + 1] : null;
    return '<div class="manual-nav' + (bottom ? ' bottom' : '') + '">' +
      (bottom ? '' : '<button class="manual-tocbtn" title="Show or hide the contents">☰</button>') +
      (prev ? '<button data-nav="' + esc(prev.id) + '" title="' + esc(prev.title) + '">‹ ' +
        esc(short(prev)) + '</button>' : '') +
      '<span class="spacer"></span>' +
      (next ? '<button data-nav="' + esc(next.id) + '" title="' + esc(next.title) + '">' +
        esc(short(next)) + ' ›</button>' : '') +
      '</div>';
  }

  function renderReader() {
    var ix = ensureIndex();
    var s = ix.byId[view.sectionId];
    var reader = view.root.querySelector('.manual-reader');
    if (!s) { reader.innerHTML = ''; return; }
    var label = Manual.label(s);
    var pages = [];
    if (s.pages && s.pages.text) {
      pages.push(s.pages.text + (s.pages.inherited ? ' (the heading above)' : ''));
    }
    if (s.group) pages.push(s.group);
    reader.innerHTML =
      navHTML(s, ix, false) +
      '<h2 class="manual-h2">' +
        (label && s.title.indexOf(label) !== 0 ? '<span class="manual-num">' + esc(label) + '</span>' : '') +
        esc(s.title) + '</h2>' +
      (pages.length ? '<div class="manual-pages">' + esc(pages.join(' · ')) + '</div>' : '') +
      '<div class="manual-body">' + (s.html || '<p class="manual-none">This heading has no text of its own.</p>') + '</div>' +
      navHTML(s, ix, true);
    var body = reader.querySelector('.manual-body');
    if (Manual.hooks.select) linkDesignators(body, s);
    if (view.query) markText(body, view.query);
    var first = body.querySelector('mark');
    if (first) revealIn(reader, first, true);
    else reader.scrollTop = 0;
  }

  function wire(root) {
    root.addEventListener('click', function (e) {
      var t = e.target;
      var li = t.closest ? t.closest('li[data-section]') : null;
      if (li) { open(li.dataset.section, li.dataset.query || ''); return; }
      var nav = t.closest ? t.closest('[data-nav]') : null;
      // Prev/next keep the highlight: the term the section was opened for is
      // as likely to be in the next paragraph as this one.
      if (nav) { open(nav.dataset.nav, view.query); return; }
      if (t.closest && t.closest('.manual-tocbtn')) {
        view.tocHidden = !view.tocHidden;
        root.classList.toggle('is-toc-hidden', view.tocHidden);
        return;
      }
      var ref = t.closest ? t.closest('.manual-ref') : null;
      if (ref && Manual.hooks.select) Manual.hooks.select(ref.dataset.ref);
    });
    root.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var li = e.target.closest ? e.target.closest('li[data-section]') : null;
      if (!li) return;
      e.preventDefault();
      open(li.dataset.section, li.dataset.query || '');
    });
    if (Manual.hooks.hover) {
      root.addEventListener('mouseover', function (e) {
        var ref = e.target.closest ? e.target.closest('.manual-ref') : null;
        if (ref) Manual.hooks.hover(ref.dataset.ref);
      });
      root.addEventListener('mouseout', function (e) {
        var ref = e.target.closest ? e.target.closest('.manual-ref') : null;
        if (ref) Manual.hooks.hover(null);
      });
    }
  }

  /* ================= text decoration ================= */

  function textNodes(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    return nodes;
  }

  /** Wrap every occurrence of `query` in the text under `root` in <mark>. */
  function markText(root, query) {
    var q = String(query || '').toLowerCase();
    if (!q) return;
    textNodes(root).forEach(function (node) {
      var text = node.nodeValue, lower = text.toLowerCase();
      var idx = lower.indexOf(q);
      if (idx < 0) return;
      var frag = document.createDocumentFragment(), pos = 0;
      while (idx >= 0) {
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        var mark = document.createElement('mark');
        mark.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(mark);
        pos = idx + q.length;
        idx = lower.indexOf(q, pos);
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      node.parentNode.replaceChild(frag, node);
    });
  }

  // The same families tools/build_manual.py recognises. Mirror any change.
  var DESIGNATOR = /\b(?:A(\d+)\s?)?(CR|VR|RT|RV|TP|DS|HR|BT|MP|XF|FL|[QRCUFWSEJPKLTH])(\d+)\b/g;

  // An assembly named on its own -- "located on A4", a table row's "A3" cell.
  var ASSEMBLY = /(^|[^A-Za-z0-9])A([1-7])(?![0-9A-Za-z])/g;

  function assembliesNamed(text) {
    var out = [], seen = {}, m;
    ASSEMBLY.lastIndex = 0;
    while ((m = ASSEMBLY.exec(text || ''))) {
      if (!seen[m[2]]) { seen[m[2]] = true; out.push('A' + m[2]); }
    }
    return out;
  }

  /**
   * Turn the designators the open board has into buttons: the manual says
   * "adjust R20", the board shows where R20 is. A designator carrying another
   * board's prefix (A4Q12 while A5 is open) stays text -- it is not on this
   * board, and a button that selects nothing would say otherwise.
   *
   * A bare designator is linked only where the manual could mean this board,
   * by the rules tools/build_manual.py resolves mentions with: not when the
   * section's heading names other boards and not this one, not when its own
   * paragraph or table row names exactly one other board (Table 4-3 lists
   * A3's TP3 in one row and A5's TP1 in the next; §4-44 says CR27 "is located
   * on A2"), and never when the section's mentions tie the designator to
   * other boards only. Every board has a TP1: a link from A3's row to A5's
   * TP1 would send the probe to the wrong board.
   */
  function linkDesignators(root, section) {
    var asm = BE && BE.state ? BE.state.assembly : null;
    if (!asm || !asm.byRef) return;
    // The boards the heading (or the ancestor heading) names, from the build:
    // when there are some, a bare designator means one of them.
    var boards = (section && section.boards) || [];
    var headingOk = boards.length ? boards.indexOf(asm.id) >= 0 : null;
    var could = {};   // bare refs the section's mentions allow on this board
    ((section && section.mentions) || []).forEach(function (m) {
      if (m.assembly === asm.id || m.assembly === null) could[m.ref] = true;
    });
    textNodes(root).forEach(function (node) {
      var p = node.parentNode;
      if (!p || /^(BUTTON|A|CODE)$/.test(p.nodeName)) return;
      var text = node.nodeValue;
      DESIGNATOR.lastIndex = 0;
      if (!DESIGNATOR.test(text)) return;
      var bareOk = headingOk;
      if (bareOk === null) {
        // No board in the heading: the paragraph or table row decides.
        var block = p.closest ? p.closest('p,li,tr,blockquote,h4') : null;
        var named = assembliesNamed(block ? block.textContent : text);
        bareOk = !(named.length === 1 && named[0] !== asm.id);
      }
      DESIGNATOR.lastIndex = 0;
      var frag = document.createDocumentFragment(), pos = 0, m;
      while ((m = DESIGNATOR.exec(text))) {
        var ref = m[2] + m[3];
        var prefixed = m[1] != null;
        if (!asm.byRef[ref]) continue;
        if (prefixed ? 'A' + m[1] !== asm.id : !(bareOk && could[ref])) continue;
        if (m.index > pos) frag.appendChild(document.createTextNode(text.slice(pos, m.index)));
        var btn = document.createElement('button');
        btn.className = 'manual-ref';
        btn.type = 'button';
        btn.dataset.ref = ref;
        btn.title = 'Select ' + ref + ' on ' + asm.id;
        btn.textContent = m[0];
        frag.appendChild(btn);
        pos = m.index + m[0].length;
      }
      if (!frag.childNodes.length) return;
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      p.replaceChild(frag, node);
    });
  }

  global.Manual = Manual;
})(window);
