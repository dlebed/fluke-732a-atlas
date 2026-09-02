/*
 * check_data.js — integrity checks over a built dataset.
 *
 * These are the mistakes that would quietly mislead someone at the bench: a
 * test point that references a COM point which does not exist, an expectation
 * with no citation back to the manual, a procedure that names a part the board
 * does not have, a link to a board that is not there. Run after any rebuild.
 *
 *   node tools/check_data.js <assembly-id>     one dataset, e.g. a3 or sys
 *   node tools/check_data.js all               every data/*.js
 */

const fs = require('fs');
const path = require('path');

const root = path.dirname(__dirname);
const dataDir = path.join(root, 'data');

// Datasets are loaded by the file name the link names, case-insensitively:
// the ids are upper case (SYS, A3) and the files are lower case (sys.js).
const datasetCache = new Map();

function datasetFile(id) {
  const want = `${String(id).toLowerCase()}.js`;
  const hit = fs.readdirSync(dataDir).find((f) => f.toLowerCase() === want);
  return hit ? path.join(dataDir, hit) : null;
}

// A dataset is a script that calls BoardExplorer.register({...}); data/ also
// holds scripts that are not datasets (data/manual.js registers the manual
// with registerManual), and those are not checked here.
const REGISTER = 'BoardExplorer.register(';

function isDataset(file) {
  return fs.readFileSync(file, 'utf8').indexOf(REGISTER) !== -1;
}

function loadDataset(file) {
  if (!datasetCache.has(file)) {
    const text = fs.readFileSync(file, 'utf8');
    const start = text.indexOf(REGISTER);
    if (start === -1) {
      throw new Error(`${path.relative(root, file)} does not call ${REGISTER}...)`);
    }
    datasetCache.set(file, JSON.parse(
      text.slice(start + REGISTER.length, text.lastIndexOf(');'))));
  }
  return datasetCache.get(file);
}

function itemsOf(data) {
  return [...(data.components || []), ...(data.testpoints || [])];
}

// An expectation is one of the five forms testpoints.js understands. Every
// one of them needs a citation; none may sit on a return or on a point that
// declares it has no published value.
function hasExpectation(st) {
  return st.nominal != null || st.maxAbs != null || st.min != null || st.max != null;
}

function check(asm) {
  const problems = [];
  const notes = [];
  const fail = (msg) => problems.push(msg);
  const note = (msg) => notes.push(msg);

  const file = datasetFile(asm);
  if (!file) {
    console.log(`no data/${asm}.js — run tools/assemble.py ${asm} first`);
    return false;
  }
  if (!isDataset(file)) {
    console.log(`data/${path.basename(file)} is not a dataset (no ${REGISTER}...) call)`);
    return false;
  }
  const data = loadDataset(file);

  const byRef = new Map();
  const all = itemsOf(data);

  // --- designators are unique -----------------------------------------------
  for (const item of all) {
    if (byRef.has(item.ref)) fail(`duplicate designator ${item.ref}`);
    byRef.set(item.ref, item);
  }

  // --- test points ----------------------------------------------------------
  for (const tp of data.testpoints || []) {
    if (tp.refPoint && !byRef.has(tp.refPoint)) {
      fail(`${tp.ref} references ${tp.refPoint} as its COM point, which does not exist`);
    }
    if (tp.refPoint === tp.ref) fail(`${tp.ref} references itself as its COM point`);

    if (tp.noPublishedValue && (hasExpectation(tp) || tp.states)) {
      fail(`${tp.ref} is marked noPublishedValue but carries an expected value`);
    }
    const states = tp.states || (tp.isReturn ? [] : [tp]);
    for (const st of states) {
      const named = st.label ? `${tp.ref} (${st.label})` : tp.ref;
      // A point can legitimately have no expected value: A5's TP1-TP14 are
      // inside a reference that is not field-repairable. That has to be
      // declared rather than left implicit, so an accidentally missing
      // nominal still fails.
      if (!tp.isReturn && !tp.noPublishedValue && !hasExpectation(st)) {
        fail(`${named} has no nominal, no ceiling and no limit`);
      }
      if (st.nominal != null && st.tolerance == null &&
          st.tolerancePct == null && st.maxAbs == null) {
        fail(`${named} has a nominal of ${st.nominal} but no tolerance`);
      }
      if (st.min != null && st.max != null && !(st.min < st.max)) {
        fail(`${named} has min ${st.min} and max ${st.max} — the band is empty`);
      }
      for (const bound of ['min', 'max']) {
        if (st[bound] != null && typeof st[bound] !== 'number') {
          fail(`${named} has a ${bound} that is not a number (${JSON.stringify(st[bound])})`);
        }
      }
      if (hasExpectation(st) && !st.source && !tp.source) {
        fail(`${named} states an expected value with no citation`);
      }
      for (const ref of st.onFail || []) {
        if (!byRef.has(ref)) fail(`${named} tells you to check ${ref}, which is not on this board`);
      }
    }
    if (tp.isReturn && (hasExpectation(tp) || tp.states)) {
      fail(`${tp.ref} is marked as a return but also carries an expected value`);
    }
  }

  // --- probe points ---------------------------------------------------------
  for (const p of data.probePoints || []) {
    if (p.component && !byRef.has(p.component)) {
      fail(`probe point ${p.id} is on ${p.component}, which is not on this board`);
    }
    if (p.refPoint && !byRef.has(p.refPoint)) {
      fail(`probe point ${p.id} references ${p.refPoint}, which does not exist`);
    }
    if (!p.source) fail(`probe point ${p.id} has no citation`);
    if (p.min != null && p.max != null && !(p.min < p.max)) {
      fail(`probe point ${p.id} has min ${p.min} and max ${p.max} — the band is empty`);
    }
  }

  // --- procedures and symptoms ----------------------------------------------
  for (const proc of data.procedures || []) {
    if (!proc.id) fail('a procedure has no id');
    for (const step of proc.steps || []) {
      for (const ref of step.refs || []) {
        // U1A..D are sections of one package, not separate designators.
        if (!byRef.has(ref) && !/^U\d+[A-D]$/.test(ref)) {
          fail(`${proc.id} step ${step.n} names ${ref}, which is not on this board`);
        }
      }
      for (const m of step.measure || []) {
        if (m.point && !byRef.has(m.point)) {
          fail(`${proc.id} step ${step.n} measures ${m.point}, which is not on this board`);
        }
        if (m.ref && !byRef.has(m.ref)) {
          fail(`${proc.id} step ${step.n} references ${m.ref}, which is not on this board`);
        }
        if (m.min != null && m.max != null && !(m.min < m.max)) {
          fail(`${proc.id} step ${step.n} has min ${m.min} and max ${m.max} — the band is empty`);
        }
      }
    }
  }
  for (const code of data.faultCodes || []) {
    for (const ref of code.refs || []) {
      if (!byRef.has(ref)) fail(`symptom ${code.code} names ${ref}, which is not on this board`);
    }
    if (!code.verdict) fail(`symptom ${code.code} has no action`);
  }

  // --- rails ----------------------------------------------------------------
  for (const [id, rail] of Object.entries(data.rails || {})) {
    if (rail.com && !byRef.has(rail.com)) {
      fail(`rail ${id} uses ${rail.com} as its COM point, which does not exist`);
    }
    for (const [group, refs] of Object.entries(rail.circuit || {})) {
      if (!Array.isArray(refs)) continue;
      for (const ref of refs) {
        // Anything shaped like a designator is held to exist -- including the
        // SYS forms A6BT1 and OUT10V -- while prose in a list is left alone.
        if (typeof ref === 'string' && /^[A-Z][A-Z0-9]*$/.test(ref) && /\d/.test(ref) &&
            !byRef.has(ref)) {
          fail(`rail ${id} lists ${ref} under ${group}, which is not on this board`);
        }
      }
    }
  }

  // --- links between datasets ------------------------------------------------
  // A link names another dataset by id and, optionally, a designator on it.
  // The target has to exist as a built file, or the button opens nothing.
  let links = 0;
  for (const item of [...all, ...(data.probePoints || [])]) {
    const link = item.link;
    if (!link) continue;
    const who = item.ref || item.id;
    links++;
    if (!link.assembly || typeof link.assembly !== 'string') {
      fail(`${who} carries a link with no assembly`);
      continue;
    }
    const target = datasetFile(link.assembly);
    if (!target || !isDataset(target)) {
      fail(`${who} links to ${link.assembly}, and there is no dataset data/${link.assembly.toLowerCase()}.js`);
      continue;
    }
    if (link.ref) {
      const there = itemsOf(loadDataset(target));
      if (!there.some((it) => it.ref === link.ref)) {
        fail(`${who} links to ${link.assembly} ${link.ref}, which is not on that board`);
      }
    }
  }

  // --- geometry -------------------------------------------------------------
  let placed = 0, verified = 0, sch = 0, notOnDrawing = 0;
  for (const item of all) {
    if (item.notOnDrawing) notOnDrawing++;
    if (item.board) {
      placed++;
      const { x, y } = item.board;
      if (!(x >= 0 && x <= 1 && y >= 0 && y <= 1)) {
        fail(`${item.ref} sits outside the board image at ${x}, ${y}`);
      }
    } else if (!item.notOnDrawing) {
      note(`${item.ref} has no board position`);
    }
    if (item.verified) verified++;
    for (const occurrence of item.sch || []) {
      sch++;
      if (!(data.schematics || []).some((s) => s.id === occurrence.sheet)) {
        fail(`${item.ref} claims to be on sheet ${occurrence.sheet}, which does not exist`);
      }
      const { x, y } = occurrence;
      if (!(x >= 0 && x <= 1 && y >= 0 && y <= 1)) {
        fail(`${item.ref} sits outside sheet ${occurrence.sheet} at ${x}, ${y}`);
      }
    }
  }
  for (const sheet of data.schematics || []) {
    if (!sheet.id || !sheet.src) fail(`sheet ${JSON.stringify(sheet.id)} has no id or no src`);
    // A sheet may have no grid; one that has must be complete.
    if (sheet.grid && !(sheet.grid.cols && sheet.grid.rows && sheet.grid.frame)) {
      fail(`sheet ${sheet.id} has a grid without cols, rows and frame`);
    }
  }

  // --- one marker sitting entirely inside another ---------------------------
  // Two parts do not occupy the same board area, so a marker wholly contained
  // in another marker is almost always one of them being in the wrong place.
  // The reader's own collision check cannot see this: it compares centres, so
  // a small box well inside a large one, off to one side, passes it cleanly.
  //
  // The exception is real and worth allowing for: a physically large part -- a
  // transformer, a big can, a connector -- covers enough board that a
  // neighbouring marker can legitimately fall inside its outline. So this
  // reports rather than fails, and says how big the container is.
  const containment = [];

  function boxesFor(space) {
    const out = [];
    for (const it of all) {
      if (space === 'board') {
        if (it.board && it.board.w && it.board.h) out.push({ ref: it.ref, g: it.board });
      } else {
        for (const o of it.sch || []) {
          if (o.sheet === space && o.w && o.h) out.push({ ref: it.ref, g: o });
        }
      }
    }
    return out.map((b) => ({
      ref: b.ref,
      x0: b.g.x - b.g.w / 2, x1: b.g.x + b.g.w / 2,
      y0: b.g.y - b.g.h / 2, y1: b.g.y + b.g.h / 2,
      area: b.g.w * b.g.h,
    }));
  }

  const spaces = ['board', ...(data.schematics || []).map((s) => s.id)];
  for (const space of spaces) {
    const boxes = boxesFor(space);
    if (boxes.length < 2) continue;
    const areas = boxes.map((b) => b.area).sort((a, b) => a - b);
    const medianArea = areas[Math.floor(areas.length / 2)];
    for (const inner of boxes) {
      for (const outer of boxes) {
        if (inner.ref === outer.ref) continue;
        const inside = inner.x0 >= outer.x0 && inner.x1 <= outer.x1 &&
                       inner.y0 >= outer.y0 && inner.y1 <= outer.y1;
        if (!inside) continue;
        containment.push({
          space, inner: inner.ref, outer: outer.ref,
          ratio: outer.area / (inner.area || 1e-9),
          outerIsLarge: outer.area > medianArea * 6,
        });
      }
    }
  }

  // --- report ---------------------------------------------------------------
  console.log(`${data.id} ${data.name}` +
              (data.pca ? ` — PCA ${data.pca}` : '') +
              (data.pcb ? ` (${data.pcb})` : '') +
              (data.rev ? ` rev ${data.rev}` : ''));
  console.log(`  ${all.length} items: ${(data.components || []).length} parts, ` +
              `${(data.testpoints || []).length} test points, ` +
              `${(data.probePoints || []).length} probe points` +
              (links ? `, ${links} links` : ''));
  console.log(`  ${placed} placed on the board, ${verified} checked by hand, ` +
              `${notOnDrawing} with no silkscreen, ${sch} schematic occurrences`);
  console.log(`  ${(data.faultCodes || []).length} symptoms, ` +
              `${(data.procedures || []).reduce((n, p) => n + (p.steps || []).length, 0)} ` +
              `procedure steps in ${(data.procedures || []).length} procedure(s)`);

  if (notes.length) {
    console.log(`\n${notes.length} items still unplaced:`);
    console.log('  ' + notes.map((n) => n.split(' ')[0]).join(' '));
  }

  if (containment.length) {
    console.log(`\n${containment.length} marker(s) sit entirely inside another — review each:`);
    for (const c of containment.sort((a, b) => a.ratio - b.ratio)) {
      console.log(`  ${c.outerIsLarge ? '·' : '⚠'} ${c.space}: ${c.inner} inside ${c.outer} ` +
                  `(${c.ratio.toFixed(1)}x its area)` +
                  (c.outerIsLarge ? ' — outer is a large part, so possible' : ''));
    }
  }

  if (problems.length) {
    console.log(`\n${problems.length} PROBLEM(S):`);
    for (const p of problems) console.log('  ✘ ' + p);
    return false;
  }
  console.log('\nAll integrity checks passed.');
  return true;
}

function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.error('usage: node tools/check_data.js <assembly-id> | all');
    process.exit(2);
  }
  let targets;
  if (arg.toLowerCase() === 'all') {
    targets = fs.readdirSync(dataDir)
      .filter((f) => /^[a-z0-9]+\.js$/i.test(f) && isDataset(path.join(dataDir, f)))
      .map((f) => f.replace(/\.js$/i, '').toLowerCase())
      .sort();
    if (!targets.length) {
      console.error('no data/*.js to check');
      process.exit(2);
    }
  } else {
    targets = [arg.toLowerCase()];
  }
  let ok = true;
  targets.forEach((asm, i) => {
    if (i) console.log('');
    if (!check(asm)) ok = false;
  });
  process.exit(ok ? 0 : 1);
}

main();
