# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`README.md` describes what the tool does and how to use it. This file covers what
is not visible from the outside: how the two halves fit together, and the
conventions that have already cost someone an afternoon. The design record is
`docs/superpowers/specs/2026-09-01-732a-atlas-design.md`; the findings from
reading the schematics by eye are `docs/review-notes.md`.

## Hard constraints

**The page must work as standalone HTML, opened straight from disk.** No build
step, no package manager, no network, no modules. `js/*.js` are ES5-style IIFEs
hanging one global off `window`; datasets are `<script src>` files that call
`BoardExplorer.register()` at load time, and the manual is one that calls
`BoardExplorer.registerManual()`. There is no `package.json` and adding one
would be a change of direction, not a convenience. Author Mode's snapping needs
the directory served (`python3 -m http.server`) because a canvas that has drawn
a `file://` image cannot be read back; it says so rather than failing silently.

**`test-logs/` and `author-exports/` are the operator's, not the tool's.**
Readings exported from the app belong to whoever measured a physical
instrument; they are gitignored. Never modify them, never let a test write there.

**Never call `localStorage.clear()`** or delete a key a test did not create. The
service log lives in local storage and there is no other copy. From `file://`
every page in the browser shares one store, so the 5700A troubleshooter's
`fluke5700a.*` keys sit beside this tool's `fluke732a.*` keys.

**The manual has no text layer, and `docs/manual/` is that text layer.** It was
made by three independent readings of every page and is the source the
datasets cite. Correct it only against the page image (`.build/pages/`), never
from memory, and keep the manual's own typos — the 1985 errata records what
Fluke corrected, `docs/review-notes.md` records what the schematics show is
wrong. `data/manual.js` is generated from it; edit the markdown, not the output.

## Commands

There is no test runner. `check_data.js` is the verification step:

```bash
node tools/check_data.js all              # or a3 | a4 | a5 | sys
```

The per-dataset pipeline, in order. Each stage has a gate; a failing gate must
not be carried forward.

```bash
tools/extract_assets.sh a3                # PDF pages -> .build/a3/*_full.png, assets/a3/*.png
/usr/bin/python3 tools/expand_parts.py a3 # data/a3.parts.raw.json -> data/a3.parts.json
/usr/bin/python3 tools/check_parts_ocr.py a3   # stock numbers vs the 600 dpi tesseract read
/usr/bin/python3 tools/ocr_designators.py a3 board   # then sh1 (minutes; tesseract)
/usr/bin/python3 tools/vlm_place.py plan a3 board    # tiles + manifest for a vision model
/usr/bin/python3 tools/vlm_place.py merge a3 board answers.json
/usr/bin/python3 tools/review_markers.py a3 board --tier vlm   # render markers to look at
/usr/bin/python3 tools/apply_review.py a3 board verdicts.json  # ok -> confirm; wrong -> re-place list
/usr/bin/python3 tools/share_interconnect.py       # SYS positions -> boards' sh2/sh3
/usr/bin/python3 tools/build_coords.py a3  # ocr + vlm + overrides -> data/a3.coords.json
/usr/bin/python3 tools/assemble.py a3      # curated + coords -> data/a3.js   (or: all)
node tools/check_data.js a3
/usr/bin/python3 tools/build_manual.py     # docs/manual/*.md -> data/manual.js
tools/make_release.sh                      # -> dist/fluke-732a-atlas.zip
```

`/usr/bin/python3` (the system 3.9) is the interpreter with PIL, numpy and
scipy; the Homebrew `python3` has none of them. ImageMagick is `magick`.
Ignore the `xcrun … cache file` noise the sandbox prints on stderr.

Positions are checked by rendering, never by reading numbers. The loop:
`review_markers.py <asm> <space> --tier <tier>` renders eight markers per
sheet → a reviewer returns `{ok, wrong, unsure}` → `apply_review.py` folds
`ok` into the overrides' `confirm` and lists the rest →
`vlm_place.py plan <asm> <space> --only R17 R13` re-reads just those → merge,
`build_coords.py`, render `--refs` and look again. Hardware with no silkscreen
(F, FL, T, XF, H, MP) always reads wrong: drop it and list it under
`notOnDrawing` instead of re-placing it.

`data/<asm>.parts.json` is regenerated from `parts.raw.json` + `parts.extras.json`
by `expand_parts.py`; a note, alias or later stock number on an existing row
goes in the extras file's `amend` list, never into `parts.json` itself.

Open one dataset directly: `index.html?assembly=A3`, plus `&author=1` for the
editor. `SYS` is the interconnect view.

## Architecture

Two halves that meet at `data/<asm>.js`.

**The engine (`js/`) is assembly-agnostic**, adapted from the 5700A
troubleshooter with these additions: one- and two-sided limits (`min`/`max`)
in `testpoints.js`; `link: { assembly, ref }` on any item, rendered as *Open
A3 ›*; the *Symptoms* tab (key `Y`) rendering the `faultCodes` array from
Table 4-2; sheets without a zone grid; ids without digits (`SYS`) sorting
first; the `vlm` placement tier; the *Manual* tab (`manual.js`, key `M`) with
manual hits in the global search and *In the manual* on every part card; and
the *Rework* tab (key `R`), the 5700A's recap round generalised to two kinds
of part — `caps.js` answers for the capacitor families, `resistors.js` for
carbon composition, and the panel branches on the family's `kind`.
`registry.js` is the whole coupling mechanism: a dataset registry, a shared
mutable `state`, and a three-function event bus; `BE.mirrors(item)` is how a
round that walks every dataset avoids counting SYS's prefixed copies of the
boards' own parts twice.

**The pipeline (`tools/`) is per-dataset and mostly Python.** Nothing is
extracted from a text layer, because there is none:

| | |
|---|---|
| Transcribed, three readers | the manual (`docs/manual/`), the parts tables (`data/*.parts.raw.json`) |
| Machine-checked | stock numbers and manufacturer codes against tesseract (`check_parts_ocr.py`) |
| Read by machine, then looked at | designator positions: tesseract where the lettering is clean, a vision model where it is not, every marker rendered back and checked |
| **Hands only** | expected voltages and their tolerances, test-point pads, what a part does, and anywhere two sources disagree |

**Generated vs curated.** `data/<asm>.js`, `data/<asm>.coords.json`,
`data/<asm>.parts.json` and `data/manual.js` are output — never hand-edit them.
The curated inputs are `<asm>.board.json`, `<asm>.parts.raw.json`, `<asm>.parts.extras.json`
(items the drawings letter but the table omits: terminals, edge connectors, A4's CR2),
`<asm>.testpoints.json`, `<asm>.procedures.json`, `<asm>.reference.json`,
`<asm>.caps.json` and `<asm>.coords.overrides.json`. `data/schema.md`
documents every field.

## Conventions that bite

**A marker's `x,y` is the box centre, not its top-left.** Any verification that
draws boxes from `x,y` as a corner will show every marker shifted.

**Override coordinates are integer pixels of `.build/<asm>/drawing_full.png`**
(3620×4552 for A3, 3600×3170 for A4, 4170×2380 for A5, 9517×5608 for the
interconnect), not the browser image. `tools/fold_overrides.py` converts an
Author Mode export; do not convert by hand.

**The reader is not deterministic.** `.build/<asm>/ocr_*.json` and
`vlm_*.json` are versioned on purpose: the overrides name dropped and
confirmed markers against exactly those reads.

**Figures 8-1 and 8-2 are shared.** `SYS` owns the crops (`assets/sys/`); A3,
A4 and A5 name the same files as their `sh2`/`sh3` and `.build/<asm>/sch2_full.png`
is a symlink to the `sys` crop. Positions on the interconnect are read once
for `SYS` (with assembly-prefixed refs, `A3TP1`) and copied to the boards'
`sh2` by `tools/build_coords.py`.

**The manual disagrees with the drawings in places, and the drawings with
each other.** A3 CR17 (parts list, drawing) is CR23 on the schematic; A4's
parts-list CR4 is the CR2 the drawing and schematic print; Figure 8-1 letters
A3's R20 as "R50"; A3 R11 is 12.7 kΩ in the table and 6.65 kΩ on the sheet;
the 1985 errata renames A4/A5 zeners to VR designators from Rev C. Every one
is a caveat in the dataset — record, do not "fix".

**A reference table's keys are its column headings** (`tables[].rows`), unless
the table says `headerRow: true` and its first row is the heading (the SYS
signal map). **`virtual: true`** in `board.json` keeps a dataset (SYS) out of
the log's fitted-board list. **`aliases`** on a part (VR1 for CR1, "R50" for
R20) are searchable; the card says which name is which.

**Never write synthetic test data into `.build/<asm>/` or `data/<real id>.*`.**
A reviewer's smoke test once overwrote `.build/a3/drawing_full.png` with a
1200 px placeholder and every A3 tile had to be regenerated. Use a scratch id
(`zz`) and delete it afterwards.

**`check_parts_ocr.py` differences are almost always tesseract glyph slips**
(O/0, Y/4, S/5, a mis-split `R61` → `R6 1`); read the row on the page before
changing the transcription.

**A parts-table description is punctuated three ways**, and everything that
reads a value out of one goes through `Parts.spec` / `ratedVoltage` /
`ratedPower`, never its own regex: the tolerance is `+/-20%` (not the 5700A's
`+-20%`) and shares the value's comma-field; an asymmetric pair is slashed and
prints in either order (`+75/-20%`, `-20/+75%`); a full stop can stand in for
a comma (`CAP, CER. 0.22 UF`, `RES, MTL. FILM`); and a curated row appends its
own note after `" - "`, which `Parts.listText` cuts off first. `CAP, ELECT` is
an aluminium can and `RES, COMP` is carbon composition — the two families the
*Rework* round is about. See `docs/review-notes.md`.

**Starred rows are the reference**, which §4-53 says is not field repairable
(A5 R24/R25/R26/R62/R63/R64 among the carbon comps). `star` survives into the
dataset; anything that ticks parts in bulk must skip them.

**A panel section's header is one line, and `.readings th` depends on it.**
`section(title, meta, body, cls)` builds a sticky `--panel-head-h` header, and
the column labels pin themselves exactly that far down; a header that wraps is
painted over them rather than pushing them aside. Anything whose title is prose
passes `'is-table'`, which unsticks the header, lets it wrap, and puts the
table in a sideways-scrolling strip. Inside that strip the labels must be
`position: static` — sticky is scoped to the nearest scrollport, so an
inherited `top` offset displaces them down over the table's first row.

**`refs.locator` and `refs.parts` print in the footer cut at the first comma**,
with the whole string on hover, so put the figure or table number before that
comma and the page numbering after it. They have no other consumer.

**Storage keys are versioned and unit-scoped** (`fluke732a.testlog.v2`,
`.notes.v2`, `.units.v1`, …). Everything recorded belongs to one 732A
identified by its serial. `units.js` must load before `notes.js` and
`testlog.js`, which is why `index.html` orders them that way.

**Table 4-3 prints no tolerances** for 32 V, 33.0 V and 18.5 V. The ones in
`testpoints.json` are assumptions marked `inferred: true` with a note; the
app shows the flag. Do not quietly tighten or loosen them.

## Testing in the browser

Serve the directory (`python3 -m http.server 8732 --bind 127.0.0.1`) and drive
Chrome through the DevTools MCP tools; also open `index.html` from `file://`,
because the two origins differ in what they allow. Things that trip a script:
keyboard shortcuts must be dispatched as `keydown` on `document` with the
search box blurred (a focused search box swallows `1`–`6`); switching modes
needs the tab button clicked, not `BoardExplorer.set({mode})`; reference
tables render in the Symptoms panel. Every `file://` page in the browser
shares one localStorage, so a synthetic unit left by a test shows up in the
real tool — remove only the keys the test created.

Layout is checked by numbers, not by looking — the inverse of positions.
Compare `getBoundingClientRect()` edges for overlap, `scrollWidth > clientWidth`
for clipping, and sweep all four assemblies against all seven tabs in one
`evaluate_script`; a screenshot shows that something is wrong, not what.

## Binaries live in Git LFS

`.gitattributes` routes `*.png`, `*.jpg`, `*.zip` and `*.pdf` through Git LFS:
the board drawings and sheets under `assets/` and the brand design package.
Clone with `git lfs` installed or the images arrive as pointer files and the
page shows empty stages. `tools/make_release.sh` copies the working-tree
files, so it needs a checkout with the LFS content present.

## The manual lives outside the repo

`tools/extract_assets.sh` resolves the PDF as `../732A-manual.pdf` (or
`$MANUAL`). Without it the app works completely; only re-extraction does not.
