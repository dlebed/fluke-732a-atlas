# Fluke 732A Atlas — design

A bench tool for servicing the Fluke 732A DC Reference Standard, built from the
5700A Interactive Troubleshooter's engine. Same functionality — find a part,
know what a test point should read, follow a procedure, record what was
measured against one physical unit, replace parts, author positions — for a
much simpler instrument: three boards and a system interconnect view.

Source: `732A-manual.pdf` (P/N 645051, May 1983, 94 pages, 600 dpi scan, **no
text layer**). Everything is read by OCR or by eye and then checked by a second
reader; the transcriptions become the text layer the manual lacks and are
versioned under `manual-text/`.

## Scope

| Dataset | Name | Drawing | Schematic sheets | Parts list |
|---|---|---|---|---|
| `A3` | Pre-Regulator PCB Assembly (732A-4003) | p88 Fig 8-3 | p89 (sh1), p85 interconnect (sh2), p87 motherboard/battery (sh3) | Table 5-4, p54–55 |
| `A4` | Regulator PCB Assembly (732A-4002) | p90 Fig 8-4 | p91 (sh1), p85 (sh2), p87 (sh3) | Table 5-5, p58–59 |
| `A5` | Reference PCB Assembly (732A-4001) | p92 Fig 8-5 | p93 (sh1), p85 (sh2) | Table 5-6, p60–62 |
| `SYS` | 732A System interconnect | p85 Fig 8-1 (the interconnect diagram *is* the "board") | p87 Fig 8-2 schematic (sh1), p86 Fig 8-2 board outlines (sh2) | none — items are what the diagrams draw |

Page numbers are PDF pages. Board drawings are cropped to the PCB outline
(with a small margin), never the whole page; schematic sheets and the two
diagrams are cropped to the figure's drawn frame. No photographs exist yet:
the engine already greys out Photo / Overlay / Swipe when a dataset has no
photo layer, and the photo slot stays in the schema for later.

### How the interconnect diagrams are used

Figure 8-1 (p85) and Figure 8-2 (p87) are simplified, high-level and omit
parts; they are still the fastest way to see how a signal crosses from one
board to another. Two uses:

1. **A System entry in the assembly picker** (`SYS`, listed first). Its drawing
   is Figure 8-1. Markers sit on each assembly block (A3, A4, A5, A6 battery
   pack, A1 LED board, front panel) and carry a `link` to that assembly, so
   clicking a block and pressing *Open A3 ›* on the card opens the board.
   Connectors (A2 J2/J3/J4, A3 P3, A4 P2, A6 P4), the battery pack parts
   (BT1–BT4, CR1, R1, DS1 ballast lamp, RT1, RT2), the oven heaters HR1–HR4
   and oven thermistors RT3/RT4, and the front-panel LEDs are items too, with
   refs prefixed by their assembly (`A6BT1`, `A1DS2`, `A2J3`) so nothing
   collides with a board's own designators. SYS carries the front and rear
   panel rows of Table 4-3 as its test points (`OUT10V`, `OUT1V`, `OUT1018`,
   `EXTPWR`), the whole of Table 4-2 as its symptoms, and the whole of Table
   4-3 as a procedure whose steps name the board each measurement is on.
2. **An extra sheet on each board.** Every board's own designators that
   appear on Figure 8-1 are placed on it as sheet `sh2` ("Interconnect"), and
   on A3/A4 Figure 8-2 is `sh3` ("Motherboard, battery and LED PCBs"), so the
   schematic jump can turn to the sheet where the board meets its neighbours.
   A caveat on each board says the diagram is simplified.

## Data per board

**Test points** (`data/<asm>.testpoints.json`, hand-curated, every value cited):

| Board | Point | Reference | Expected | Source |
|---|---|---|---|---|
| A3 | TP3 | TP4 | ≤ 60 V dc (rectified raw) | Table 4-3 |
| A3 | TP6 | TP4 | 32 V dc (pre-regulator out) | Table 4-3, §4-44 step 18 |
| A3 | TP2 | TP1 | ≤ 31 V dc (charger; 24.5–26.5 V at BTRY CHG on, >31 V off) | Table 4-3, §4-44 steps 16–21 |
| A3 | TP5 | TP1 | 33.0 V dc (set by R20) | Table 4-3, §4-44 step 10 |
| A3 | TP1, TP4 | — | returns | schematic p89 |
| A4 | TP1 | TP3 | 32 V dc | Table 4-3 |
| A4 | TP1 | TP2 | ≈ 18.5 V dc (schematic prints 18.6 V) | Table 4-3, Fig 8-1 |
| A4 | TP2 (COMMON), TP3 | — | returns | schematic p91 |
| A5 | TP1–TP14 | — | `noPublishedValue`: the reference is not field-repairable (§4-53, Table 5-6 note) | §4-53 |
| SYS | OUT10V / OUT1V / OUT1018 vs COM | — | 10.00000 / 1.000000 / 1.018000 V, tolerance from Table 1-2 | Table 4-3, Table 1-2 |
| SYS | EXTPWR (rear) | — | ≥ 24 V dc | Table 4-3 |

Table 4-3 gives no tolerance for 32 V, 33.0 V or 18.5 V. Those entries carry an
assumed tolerance marked `inferred: true` with a note saying so; the user can
edit it in Author Mode. The one-sided limits need a new expectation form (see
engine changes).

**Reference** (`data/<asm>.reference.json`): overview from §3 theory, rail
circuits (which rectifier/filter/regulator makes which rail, with the test
points on it), part functions where §3 states them, `faultCodes` filled from
Table 4-2 rows that point at the board (rendered under a **Symptoms** tab),
warnings (§4-51 shock hazard; battery peak current; A5 oven repair caution),
caveats (interconnect simplified; Table 4-3 tolerances assumed).

**Procedures** (`data/<asm>.procedures.json`): A3 — §4-44 Battery Charger
Adjustment, 26 steps with refs and the measurements each step asks for; A3 and
A4 — their rows of Table 4-3 as an "Internal voltage measurements" procedure;
SYS — the full Table 4-3, plus the §4-32 calibration procedures (A and B) if
the transcription is clean enough to be trusted. A5 — none.

**Parts** (`data/<asm>.parts.json`): the parts table transcribed twice
(tesseract at 600 dpi, and a vision model reading the page) and diffed; every
disagreement resolved by looking at a crop. Same fields as the 5700A's
`extracted.json` components: `ref, kind, desc, fluke, mfrCode, mfrPart, qty,
notes`. Ranges like `CR5-CR9`, `TP1-TP6`, `R50-R53` are expanded. Starred rows
in Table 5-6 keep the `*` note ("return to Fluke or replace the whole
reference PCB").

**Caps** (`data/<asm>.caps.json`): rail each electrolytic/tantalum sits on,
traced on the sheet; `appliedV` from Table 4-3 where published, else inferred
with the reasoning in the note, else null.

**Coordinates**: `tools/ocr_designators.py` + `build_coords.py` as in the
5700A, then a vision pass for what tesseract cannot read on these hand-lettered
drawings (`tools/vlm_place.py plan|refine|merge`: tiles with a labelled grid,
a model names each designator's centre, a connected-component refinement snaps
the box to the ink), then every marker rendered back and reviewed by eye
(`review_markers.py`), corrections into `data/<asm>.coords.overrides.json`,
loop until a review round finds nothing. Test points are placed by hand on the
pad, `shape: point`.

## Engine changes (all of them)

The engine is copied from the 5700A troubleshooter and stays assembly-agnostic.
These are the only changes:

1. **Rebrand.** Title "732A Atlas", brand model "732A", storage prefix
   `fluke732a.` everywhere (`testlog`, `notes`, `units`, `author`, `sync`,
   `capaudit`, …), service-log `format` string `fluke732a-servicelog`, default
   unit model `732A`, report footer and export file names. The service log
   import refuses 5700A files by format string, as before.
2. **Symptoms tab.** The tab labelled *Fault codes* (key `F`) is labelled
   *Symptoms*; it renders the same `faultCodes` array. Each entry: `code` (a
   short id), `title` (the symptom), `measure` (probable cause), `verdict`
   (action), `refs`, `source: 'Table 4-2'`. Empty-state wording changes to
   match.
3. **One-sided and two-sided limits.** `testpoints.js` accepts `{ min }`,
   `{ max }` and `{ min, max }` alongside `nominal/tolerance`,
   `nominal/tolerancePct` and `maxAbs`. `range()` returns `lo/hi`; nominal is
   the midpoint of a two-sided range and the bound itself for a one-sided one.
   `evaluate()`: outside → fail; inside but within 10 % of the band width (or
   5 % of the bound for one-sided) of a limit → marginal; else pass.
   `formatRange()` prints `≤ 60 V`, `≥ 24 V`, `+24.5 … +26.5 V`.
   `check_data.js` treats min/max as an expectation.
4. **Links between datasets.** An item may carry `link: { assembly: 'A3',
   ref: 'TP1' }`. The card shows *Open A3 ›*; pressing it switches the
   assembly and selects `ref` if given.
5. **Picker order.** `registry.list()` puts ids with no number (`SYS`) first,
   then numeric order.
6. **Sheets without a zone grid.** A sheet may omit `grid`; nothing derives a
   zone for it and the zone label is simply absent.
7. **Kinds.** New designator families → kinds: `DS` led, `T` transformer, `S`
   switch, `W` wire, `RT` thermistor, `FL` part, `XF` mech, `J`/`P` connector
   (J is a connector on this instrument, not a jumper), `E` **terminal** (new
   kind: harness feed-through and solder terminals), `BT` battery, `HR`
   **heater** (new kind). New kinds get all three maps in `app.js`.
8. **Author Mode without a photograph.** The landmark / align-outline tools
   say the board has no photograph instead of failing.

## Pipeline

```
tools/extract_assets.sh <asm>     pdftoppm 600 dpi -> .build/<asm>/drawing_full.png, schN_full.png
                                  -> assets/<asm>/drawing.png (3000 px wide), schN.png (3600 px wide)
tools/ocr_parts.py <asm>          tesseract over the parts-table pages -> .build/<asm>/ocr_parts.txt
tools/ocr_designators.py <asm> <space>
tools/vlm_place.py plan|refine|merge <asm> <space>
tools/build_coords.py <asm>
tools/assemble.py <asm>           data/<asm>.{parts,procedures,testpoints,reference,caps,coords}.json -> data/<asm>.js
node tools/check_data.js <asm>
tools/fold_overrides.py / fold_bundle.py   Author Mode exports -> overrides
tools/make_release.sh             -> dist/fluke-732a-atlas.zip
```

`assemble.py` reads the curated parts and procedures files directly; there is
no `build_data.py` because there is no text layer to parse. The manual is
resolved as `../732A-manual.pdf` relative to the repository, and is not
redistributed.

## Layout

```
index.html  css/  js/                  engine (rebranded copy)
data/<asm>.{js,coords.json}            generated
data/<asm>.{parts,procedures,testpoints,reference,caps,coords.overrides}.json   curated
data/schema.md
assets/{a3,a4,a5,sys}/                 drawing.png, sch1..N.png
assets/brand/
manual-text/                           transcriptions of the manual sections used, with page refs
tools/                                 pipeline
.build/<asm>/                          full-resolution crops (ignored) and reader output (kept)
docs/superpowers/specs/                this document
README.md  CLAUDE.md  CREDITS.md  LICENSE  .gitignore
```

## Verification

- `node tools/check_data.js` passes for all four datasets.
- Every transcription and every curated value is checked by a second,
  independent reader against the page image; disagreements are resolved by a
  third look at a crop, never by majority guess.
- Markers reviewed visually, tier by tier, until a review round finds no
  error.
- Browser test on the real page (served and from `file://`): search, board /
  schematic / split, test points with a recorded reading scored, the A3
  procedure with a measurement recorded, a symptom, a part marked replaced,
  a note, export and re-import of the service log, Author Mode drag and
  export, the SYS links, both linked-view directions.

## Out of scope

Photographs; A1, A2, A6, A7 as full datasets (A6/A1 items appear on SYS only);
a text search of the manual; anything the 5700A tool does not do.

## Addendum (same day): the manual inside the tool

The primary use is a technician troubleshooting, repairing and servicing
several 732A units with nothing else open. So the transcribed manual is not
only kept under `docs/manual/` for the pipeline — it ships inside the page:

- `tools/build_manual.py` turns `docs/manual/*.md` into `data/manual.js`,
  which registers the manual as sections: `{ id, title, section ('3-10'),
  pages, html, text, mentions: [{ ref, assembly? }] }`. Markdown is converted
  at build time (headings, paragraphs, tables, bold, lists) — no runtime
  markdown library.
- A **Manual** mode (key `M`) shows the table of contents, a section reader
  with the page reference on every heading, and an in-manual search box.
  The global search shows manual hits below part hits ("in the manual: §3-11
  Power Supplies…"), and selecting one opens the section with the term
  highlighted.
- A part's card carries **In the manual**: the paragraphs that name it.
  Mentions are resolved to an assembly when the paragraph's heading or the
  text names one (`A4Q12`, "Pre-regulator (A3Q1)", a heading "(A3 and A4)");
  otherwise the mention is shown as unresolved and appears on every board
  that has the designator, marked as such.
- The errata sheet is a section of its own and its changes are also
  reflected in the datasets (aliases, added parts, corrected procedure text).

Also carried into the datasets from the errata: A3 R19 (Rev F), A4 VR1/VR2/VR9
and A5 VR1/VR2/VR6/VR8 aliases (Rev C), the A5A8 piggyback divider (Rev E),
§4-55 divider repair, §4-45 step 27 and §4-45A charging notes, the thermal
fuse F2, and the J10 external power connector.
