<img src="assets/brand/lockup-dark.svg" alt="Atlas — 732A service" width="240" height="72">

# 732A Atlas

A bench tool for servicing the Fluke 732A DC Reference Standard: find a part on
the board, see what a test point should read and what to reference it against,
follow the manual's procedures, read the manual itself, and record what you
measured against each instrument so the readings are still there next year.

Standalone HTML: open `index.html` in a browser and it works. No server, no
build step, no install, no network.

Covers the three plug-in boards — **A3 Pre-Regulator** (mains input,
pre-regulator and battery charger), **A4 Regulator** (18.6 V regulator,
voltage monitor / IN CAL latch, oven heater driver) and **A5 Reference** (the
ovenised 10 V reference, output dividers and oven controller) — plus a
**System** view built on the manual's interconnect diagram, where every block
and every inter-board signal is clickable and leads to the board it belongs
to. The engine is assembly-agnostic — each board is a data file plus its
images — and it is the engine of the Fluke 5700A Interactive Troubleshooter.

![The A3 Pre-Regulator board with CR15 selected: the drawing with every
designator boxed and colour-coded by component type, and a card giving the
parts-list entry, the manual paragraphs that mention the part, and a box to
record what the meter read](docs/screenshots/board.png)

*A3 with CR15 picked out. Type a designator, a signal name, a value or a Fluke
stock number and the board goes to it; the card carries what the parts list
says, where the manual mentions it, and somewhere to put your reading.*

---

## Safety and disclaimer

**Read this before opening the instrument.**

### Mains, and a battery that can weld

The A3 Pre-Regulator carries the **ac line**: the power connector, fuse
holder, line filter and transformer primary are live whenever the cord is in,
and the line-voltage selection switches sit on that board. The manual's own
warning (§4-51): do not perform these tests alone, remove jewellery, and
exercise appropriate caution around the ac power connector, fuseholder and
power transformer.

The internal **24 V lead-acid battery pack can deliver extremely high peak
currents**. Avoid accidental shorting of battery terminals, and keep the pack
upright (the 1985 errata's caution).

Opening, servicing or repairing the instrument is done entirely at your own
risk.

### The reference is not meant to be repaired

The manual (§4-53) says the reference circuit inside the oven — U1, U2, Q1,
Q2, Q5 and the resistors at TP11–TP14 on A5 — is not field-repairable and the
oven assembly is exchanged as a unit; the 1985 errata later allowed repair of
the 1 V / 1.018 V divider strings with a trim-resistor selection procedure.
The atlas documents A5 so its parts can be found and its nets understood; it
does not encourage working on it.

### The information here may be wrong

This tool is provided **as is**, with no warranty of any kind. Its data is
derived from a scanned 1983 manual with no text layer by transcription,
optical character recognition and hand correction, and any part of it may be
inaccurate, incomplete or out of date — a misplaced marker, a mistyped
value, a net traced to the wrong terminal. Where the manual disagrees with
its own drawings, the atlas records both and says which it followed
(`docs/review-notes.md`).

Use it at your own risk, and **cross-check anything that matters against the
official Fluke documentation** before acting on it.

### No liability

The author accepts no responsibility or liability whatsoever for any direct,
indirect, incidental or consequential damage, loss, injury or other
consequence arising from the use of this tool or of the information in it,
however caused. See `LICENSE` for the full terms.

---

## What it does

**Find a part.** Type a designator (`CR15`), a signal name (`+RAW`), a value
(`4700 PF`), a Fluke stock number (`334839`) or a manufacturer part number.
The board pans and zooms to it; partial matches highlight every hit. Harness
terminals (`E9`), edge connectors (`P3`) and parts the drawings letter but the
parts list omits (A4's CR2) are searchable too, marked as such.

**Know what to expect.** Test point mode shows the test points coloured by
rail, each with its expected reading, the point to reference it against, the
condition it holds under and the table or paragraph the value came from. The
732A manual publishes few numbers (Table 4-3: ten rows), so where a tolerance
is assumed the point says *inferred* and where none is published it says so
rather than showing a guess. One-sided limits (`≤ 60 V`, `≥ 24 V`) are scored
as such.

**Record measurements.** Start a session, click a point, type what your meter
reads; the tool scores it, colours the marker, and keeps it per instrument.
Components can be measured too (resistance, capacitance, ESR, forward drop…),
scored against their own parts-list value where it states one.

**Follow the procedure.** A3 carries §4-44, the Battery Charger Adjustment,
with every step's measurement scored as you go, the 1985 errata's corrections
and its added step 27; each board carries its rows of Table 4-3 as an
*Internal voltage measurements* procedure; the System view carries the whole
of Table 4-3, the acceptance test, null verification and calibration
Procedures A and B.

**Start from a symptom.** The *Symptoms* tab is Table 4-2: what the
instrument does, the probable cause, the action — pointing at the parts
involved.

**Read the manual.** The *Manual* tab is the whole instruction manual and the
1985 change/errata sheet, transcribed, searchable, with the page reference on
every heading. The global search shows manual hits below part hits, and every
part's card lists the paragraphs that mention it.

**See how the boards connect.** The System entry's drawing is Figure 8-1, the
interconnect diagram: click the A3 block, or any of the A3 test points drawn on
it, and *Open A3 ›* takes you to the board with that point selected. The same
figure is each board's second schematic sheet, so a board's designators can be
followed off the board onto the harness. Figure 8-2 (motherboard, battery
module, LED board) is the third. Both are the manual's simplified diagrams,
and the atlas says so.

**Look at it however helps.** Board drawing, any schematic sheet, or board and
schematic side by side with the selection synchronised; `S` jumps between
them. *Linked view* opens a follower window for the other monitor.

**Write things down.** Any part or test point takes free-text notes, kept
apart from the dataset so a rebuild never loses them.

**Plan a rework round.** The *Rework* tab is the parts-replacement job in one
place: tantalums ranked by how close the rail runs to their rating, aluminium
cans by size and by how much capacitance they have measurably lost, and the
732A's 45 carbon composition resistors — 43 on the three boards, plus the
front panel's and the battery board's — the family that drifts up with age,
ranked by what has already measured out of tolerance, then by value, because
the megohm positions move furthest. Tick what you plan to change on any board
and *Replacement BOM* exports one order for the whole instrument, capacitors
grouped by the rating to fit and resistors by value, tolerance and wattage.

Work a row and it records itself: measure the part in or out of circuit and
the reading is scored against the parts list (`+9.2% of 91 kΩ — outside ±5%`),
mark it removed, then enter what went in — part number, value, tolerance and
wattage for a resistor, value, rating and ESR for a capacitor — and the new
part is checked against its own nominal before it is soldered in. All of it
lands in the unit's log and prints in the service report. Carbon film (A3 R19)
and deposited carbon are classified but never swept into the round: they are
film on ceramic, and stable. Six of A5's carbon comps are inside the reference
that §4-53 says is not field repairable; they stay visible, marked, and no
bulk tick will put them in an order.

### The service record

Everything you record belongs to **one 732A, identified by its serial** —
readings, repairs and notes alike. Several units on the bench are ordinary;
the unit picker keeps them apart. *Mark suspect*, *Mark faulty* and
*Replaced…* live on the part's card; the replacement is prefilled from the
parts list and flagged when it is a substitute. *Export log* writes one JSON
file per unit; *Open a log…* merges one back in without replacing anything.
The *Service report* is a standalone printable HTML page.

### Keyboard

| Key | |
|---|---|
| `/` | search |
| `B` `T` `L` `P` `Y` `M` `R` | board · test points · log · procedure · symptoms · manual · rework |
| `1`–`6` | drawing · photo · overlay · swipe · schematic · split (photo modes are disabled until a board has a photograph) |
| `S` | show the selection on the schematic |
| `V` | focus the measurement box |
| `Z` | fit to view |
| `Esc` | clear selection |

### What the other modes look like

![Test point mode on A3: the test points coloured by rail on the board, and a
panel listing them by supply with the expected reading, what to reference each
against, and the rail's rectifier, filters and regulators](docs/screenshots/testpoints.png)

*Test points, grouped by rail. Each carries its expected reading and the point
to measure it against — `≤ 60 V`, `+32 V ± 1.6`, or `return` — and says which
table or paragraph the number came from.*

![The System view: Figure 8-1, the interconnect diagram, with every block and
inter-board signal boxed, beside a parts list of the assemblies A1 through A7
and the front and rear panels](docs/screenshots/sys.png)

*The System view is Figure 8-1. Click the A3 block, or any A3 test point drawn
on it, and* Open A3 › *takes you to the board with that point selected.*

![The Rework tab on A5: the carbon composition family selected, twenty
positions on the board ranked by value from 27 MΩ down, each with a tick box,
and a Replacement BOM button](docs/screenshots/rework.png)

*The Rework tab, here on A5's carbon composition resistors — ranked by what has
already measured out of tolerance, then by value, because the megohm positions
drift furthest. Tick what you plan to change and* Replacement BOM *exports one
order for the whole instrument.*

---

## Where the data comes from

Everything is traceable to a printed page, and the app shows the citation.
The manual is the *732A DC Reference Standard Instruction Manual*, Fluke P/N
645051, May 1983, plus *Change/Errata Information Issue No. 3*, 7/85.

| Data | Source |
|---|---|
| Board drawings | Figures 8-3, 8-4, 8-5 (PDF pages 88, 90, 92), cropped to the PCB outline |
| Schematics | the same figures' second sheets (PDF pages 89, 91, 93) |
| Interconnect and motherboard diagrams | Figures 8-1 and 8-2 (PDF pages 85–87) |
| Parts lists | Tables 5-4, 5-5, 5-6 (PDF pages 54–62), transcribed twice and machine-checked |
| Expected voltages | Table 4-3 (PDF page 42), §4-44, §3, Table 1-2, the errata |
| Symptoms | Table 4-2 (PDF page 41) |
| Procedures | §4-30 – §4-45 and the errata's additions |
| Theory, functions, rails | §3 and the schematics |
| Revision levels | Table 7A-1; later revisions from the errata |

The manual is a scan with no text layer. Its transcription — three
independent readings of every page — lives in `docs/manual/` and is what the
Manual tab shows; `docs/manual/README.md` says how it was made and how far to
trust it. `docs/review-notes.md` lists what reading the schematics turned up:
A3's CR17/CR23 and R11, A4's CR2/CR4, Figure 8-1's "R50", the zeners the
errata renamed to VR designators.

### How positions were arrived at

The drawings are hand-lettered, so tesseract read about 40 % of the
designators; a vision model read the rest from gridded tiles; and **every
marker was then rendered back onto the drawing and checked by eye**, tier by
tier. The app tells you which of these a marker's position came from:

| | |
|---|---|
| **checked by hand** | a reviewer confirmed the box sits on that designator's lettering, or placed it |
| **passes agreed / uncertain / unconfirmed** | the tesseract tiers, where no reviewer has confirmed yet |
| **read by a vision model** | placed from the tiles, not yet confirmed |

Parts with no lettering on the drawing (screws, heat sinks, the transformer,
fuse and filter on A3, the E terminals that exist only on the schematic) stay
in the parts list and remain searchable; the card says there is nothing on the
drawing to point at.

There are no photographs yet. The `photo` layer is in the schema and Author
Mode can align one when a board is photographed.

---

## Editing: Author Mode

Open `index.html?author=1`, or press the *Author* tab. Drag a marker to move
it, use the handles to resize, arrows to nudge, `Del` to redraw; the inspector
edits every field of a test point including one-sided limits. *Export
coordinates* writes the board's `coords.json`; fold it into the overrides so
it survives a rebuild:

```
/usr/bin/python3 tools/fold_overrides.py a3 ~/Downloads/a3.coords.json --dry-run
```

Snapping a box to the printed outline needs the page served rather than
opened from disk (`python3 -m http.server`, then `http://127.0.0.1:8000/`).

## Getting the repository

The images under `assets/` are stored with Git LFS; install `git lfs` before
cloning, or run `git lfs pull` afterwards. The release zip under `dist/` has
the real files and needs neither git nor LFS.

## Rebuilding from the manual

`tools/` holds the whole chain and `CLAUDE.md` describes it. The manual PDF is
expected at `../732A-manual.pdf` (or `$MANUAL`) and is not redistributed; the
1985 errata PDF was used for `docs/manual/errata-issue3-1985.md`. Without the
PDFs the app works completely; only re-extraction of the images does not.

```
tools/make_release.sh                 # -> dist/fluke-732a-atlas.zip, the half that runs
```

---

## Layout

```
index.html            the page; lists which datasets to load
css/app.css
js/                   the engine (see CLAUDE.md); caps.js and resistors.js
                      are the two audits behind the Rework tab
data/
  a3.js a4.js a5.js sys.js manual.js     generated — do not hand-edit
  <asm>.board.json                       identity, drawing, sheets
  <asm>.parts.raw.json                   the parts table, row for row
  <asm>.parts.extras.json                items lettered on the drawings but absent from the table
  <asm>.testpoints.json                  expected values and their citations
  <asm>.procedures.json                  steps, with the measurements they call for
  <asm>.reference.json                   overview, rails, functions, symptoms, caveats
  <asm>.caps.json                        which rail each capacitor sits on
  <asm>.coords.overrides.json            hand corrections and confirmations over the readers
  schema.md
assets/a3 a4 a5 sys/  drawing.png, schN.png
docs/manual/          the transcribed manual and errata
docs/review-notes.md  what reading the schematics by eye found
tools/                extraction, OCR, vision placement, review, assembly, checks
```

## Licence

The code — `js/`, `tools/`, the curated data files — is MIT licensed
(`LICENSE`). The drawings, schematics, transcribed text, parts lists,
procedures and expected values are derived from Fluke's manual and are not
covered by that licence; see `CREDITS.md`. This is an independent project,
not affiliated with or endorsed by Fluke Corporation.
