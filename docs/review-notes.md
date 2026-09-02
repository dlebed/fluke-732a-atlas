# Manual review notes

Running record of what was checked by eye against the scanned pages, and
what was found. Findings that affect the data are carried into the relevant
`data/<asm>.reference.json` caveats; this file keeps the evidence.

## Crops (assets)

- A3, A4, A5 board drawings: cropped to the PCB outline + 40 px at 600 dpi,
  measured by `tools/find_outline.py` and confirmed against three independent
  crops supplied by the user (proportions agree: A3 0.80, A4 1.13, A5 1.73).
  Checked visually at full size: no designator clipped, the drawing number
  and caption excluded.
- Schematic sheets and the two diagrams: cropped at the ruled frame. Checked.

## Designator disagreements found while reading the schematics

- **A3 CR17 / CR23.** Table 5-4 lists CR17 (1N4448, REF) and no CR23. The
  schematic's REF DESIG table says CR17 is *not used* and draws CR23 (a diode
  whose anode is on the Q4 *base* node -- C5 +, R15, the CR21 cathode -- and
  whose cathode is the R13 / R14 tap of the sense divider, in parallel with
  R15; an earlier note here said "Q4 collector node", corrected at 600 dpi). Figure 8-3's board
  drawing prints CR17 beside R13/R15 and prints no CR23. So the diode the
  drawing and parts list call CR17 is the one the schematic calls CR23.
- **A4 CR2 / CR4.** Table 5-5 lists CR4 (1N4571, 6.4 V temperature-compensated
  zener) and no CR2. The schematic draws CR2 as the circled reference zener
  beside C2 (82 µF) at the Q1/Q2 error amplifier and says CR4, CR5 and CR11
  are not used; the board drawing prints CR2 (in the CR6..CR9 column) and no
  CR4. So the part the parts list calls CR4 is CR2 on the board and schematic.
- **A4 CR5.** The schematic's REF DESIG table says CR5 is not used, yet the
  sheet draws CR5 (diode in series with R4 9.53 kΩ at the top) and the parts
  list carries CR5 (1N4448, REF). The table is wrong, not the drawing.
- **A4 R4 / R20 / R13 / R25 / R26 (values and wattages).** Table 5-5 (PDF
  p58–59) lists R4 as 8.66K ±1% 1/8W (330738, CMF558661F) and R20 as 8.2K
  ±5% 1/4W (160796, CB8225); the schematic 732A-1002 prints R4 "9.53K 1/8W 1%"
  (in series with CR5 at the top of the sense divider) and R20 "6.81K 1/8W 1%"
  (Q8 base to the Q4 emitter node). R13 is 1W in the table, "1/2W 5%" on the
  sheet; R25 and R26 are 1/4W in the table, "1/2W" on the sheet. Both pages
  read at 600 dpi; the errata corrects none of them. Recorded as a caveat in
  data/a4.reference.json (value per parts list, schematic disagrees).

## Test point nets (A3, read off the schematic)

- TP3: + output of bridge CR1 (top of C1, 100 µF) — raw rectified dc before
  the pre-regulator. TP4: the raw return (the node below C2/C3, i.e. −RAW).
  TP6: Q1 emitter after R1 (0.5 Ω) — +RAW at P3-2. TP2: the charger output
  line after CR26/CR14 at W1, feeding +BATTERY (P3-9/10) through CR13/CR16.
  TP5: Q6 base lead / CR28 / RT1 / R17 junction — the trickle-charge reference (the emitter goes out through CR16 to +BATTERY).
  TP1: −BATTERY (P3-17/18).
- A4: TP1 on the +RAW-side node after R1/R2 (the regulator input, REF
  SUPPLY pins 7/8 junction); TP2 = COMMON (bottom right, beside the ground
  symbol); TP3 on the −BATTERY / −RAW node (P2-21..24), i.e. the regulator's
  negative input rail.

## A5 schematic (read by eye, 3x2 tiles of 732A-1001)

- Test points: TP2 at the U2 ref-amp / R5 node before R6; TP1 after R6/R60
  (SEL) on the 10 V reference node (CR5, R9*, CR2, CR8 hang there); TP3 after
  R8 (11.42 kΩ) at R11 SEL; TP4 after R10 SEL at the top of the divider
  string; TP5 at Q3's base network; TP6 on the E9 (WHT) net at RT3; TP7–TP10
  on the thermistor bridge (RT1, RT3, RT4, R22, R28, R29); TP11 and TP12 on
  the R59/R50/R51 chain, which the 600 dpi read of the sheet shows feeding E34
  (the 1.018 V tap); TP13 and TP14 on the R56/R53/R52 chain feeding E35 (the
  1 V tap). An earlier note here had the two chains the other way round. None has a published value (Table 4-3 lists no
  A5 point; §4-53 forbids repair of the reference).
- Harness terminals to the motherboard: E1 BRN, E2 RED, E3 ORN, E4 YEL, E5
  GRN, E6 BLU, E7 VIO, E8 GRA, E9 WHT, E10 BLK, E11 BRN. Front panel: E21/E22
  THERMISTOR (RT2, 10 kΩ at 25 °C), E23/E24/E25 10V HI, E26 LO, E27/E28 LO,
  E33 10V HI, E34 1.018V HI, E35 1V HI, E36 LO. Calibration PCB (732A-1007)
  taps E14..E18 marked 40, 20, 10, 5 PPM. REF DESIGNATIONS box: highest C17,
  CR8, E36 (not used E12, 13, 19, 20, 29–32), Q5, R64, RT2, TP14, U5.
- "TERM STRIP INSIDE FRT PAN.": R1 2 Ω, CR1, RV1, DS1 (neon), C1 82 µF across
  10V HI / LO — the output protection network; these are the final
  assembly's C1, CR1 and DS1 of Table 5-1, not A5 parts.
- Values printed beside the ref-amp parts (R5*, R9*, U2*) carry the * of note
  3: "REF AMP SET 732A-4502", matching the parts list's "REF AMP SET
  (includes R5, R9 and U2)".

## Interconnect diagram, Figure 8-1 (read by eye, 3x2 tiles)

- The A3 block labels the trickle-charge potentiometer **R50**. A3 has no R50
  (Table 5-4 ends at R20; the schematic's REF DESIG box says last used R20).
  The part in that position on the schematic is R20 (50 kΩ), the pot §4-44
  step 10 sets for 33.0 V at TP5. Treat "R50" on Figure 8-1 as R20.
- A3 designators drawn on Figure 8-1: TP1–TP6, Q1, Q2, Q3, Q4, Q6, CR6, CR7,
  CR12, CR13, CR16, CR19, CR20, CR25, R1, R3, R4, R9, R10, R11, R12, R13,
  R16, R17, W1, (R50 = R20), plus the transformer, bridge and two LEDs drawn
  without designators. P3/J3 pins 1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14,
  15, 16, 17, 18.
- A4 designators drawn: TP1, TP2, TP3, Q1, Q2, Q3, Q4, Q6, Q7 (latch), Q8,
  Q12, Q13, Q14, CR2, CR13, CR14, R1, R2, R3, R4, R7, R8, R9, R21, R22, R24,
  R25, R26. P2/J2 pins 1–27 (5, 12, 17, 25 NC).
- A5 designators drawn: U1, U2, U5, Q1, Q2 (as "series pass drive
  transistors"), R2, R3, CR2, CR5, RT2, RT3, RT4, the three ADJ pots, E1, E2,
  E3, E8, E9, E10, E11, E21–E28, E33–E36. "18.6V" printed on the E8 (GRA)
  net and on the A4 regulator output.
- A6 battery pack: BT1–BT4 in holders J1–J4, CR1, R1, DS1 (ballast lamp),
  RT1, RT2, BAT ON/OFF switch, BLK/RED rear-panel POWER INPUT terminals,
  P4/J4 pins 1–6. Front panel: GUARD (BLU), GROUND (GRN/YEL), DS1 AC PWR
  (RED 12 / ORN 13), DS2 BTRY CHG (VIO 17 / GRA 18), DS3 IN CAL (YEL 14 /
  BLU 16), RESET (GRN 15), 10V HI, 1.018V HI, 1V HI, LO, OVEN TEMP THMS
  (GRA, E21/E22).

## Transcription spot checks

- `01-specifications.md` Table 1-2 against PDF p10–11: every figure agrees
  (transfer uncertainty, temperature coefficients, adjustment ranges, line
  power table, auxiliary power, battery). Table 1-1 prints the full-width
  rack mount kit as M07-200-601 while the Section 6 heading in the table of
  contents prints M07-200-603 — checked below.
  Result: the manual is inconsistent with itself — Table 1-1 (PDF p9) prints
  M07-200-601 and both the table of contents (p4) and §6-7 (p67) print
  M07-200-603. The transcription is faithful; nothing to fix.

## Errata / change sheet Issue 3 (7/85) — what it changes for A3, A4, A5

Read from docs/manual/errata-issue3-1985.md (verified transcription of the
separate 18-page PDF). Items that alter the atlas data:

- **A3 Rev E** (Change #4): R1 stock number 212191 → 717892 (same part).
- **A3 Rev F** (Change #10): adds R19 (RES, CF, 15K ±5%, 1/4W, 348854) to the
  charger (Figure 12 shows R19 between R18 43.2K and R20 50K); corrects the
  schematic's R8 value to 402 Ω (the parts list already says 402). Figure 12
  also confirms **CR23** on the A3 schematic and shows CR28 (".47 mA"), CR22
  and CR10 ("1 mA") as current-regulator diodes.
- **A4 Rev C** (Change #2): CR1, CR2, CR9 → VR1, VR2, VR9, all 1N5240 (qty 3).
  So the board's CR2 is a 1N5240 zener; the 1983 parts list's CR4 (1N4571,
  6.4 V) is not renamed and stays unexplained by the drawing. Record as a
  caveat; do not guess.
- **A4 Errata #4**: Figure 8-4 latch circuit redrawn; the pin list now reads
  16 = +BRIDGE, **12 = +18.6V** (the 1983 sheet prints P2-12 as NC), 18 = IN
  CAL LED, 20 = COMMON.
- **A5 Rev C** (Change #1): CR1, CR2, CR6, CR8 → VR1, VR2, VR6, VR8 (zeners).
  **A5 Rev B/C** (Change #2, second part): Figure 5-6 REF DES CR1, CR2, CR9 →
  VR1, VR2, VR9 (as printed — A5 has no CR9; transcribed as printed).
  **A5 Rev D** (Change #3): R13 stock number 213934 → 711184. **Change #8**:
  R8 divider set 346304 → 715706. **A5 Rev E** (Change #9): adds the A5A8
  piggyback PCB (751560) carrying the 1 V / 1.018 V divider taps, J1–J5, and
  matched sets R44/R46 (751917) and R45/R47 (751925); Figures 5-6 and 8-5
  replaced (Figures 9 and 10 of the errata).
- **§4-55 / 4-56 (new)**: the 1.0 V and 1.018 V divider strings ARE field
  repairable (R44/R46, R45/R47 sealed resistors; trim R50–R53 selected from
  Table 4-4 at oven temperature via TP11/TP12 and TP13/TP14; adjust R59 /
  R58). This qualifies §4-53's "not field repairable" and belongs in A5's
  procedures with the errata as its source.
- **§4-45 step 12** (Errata #8): "Remove jumper W1 on A2" → **A3**. Also
  §4-45's first sentence: Figure 4-8 → Figure 4-12.
- **§4-45 step 27** (Errata #12): trickle-charge voltage at the rear-panel
  J10 connector 25.8–27 V with a known-good battery pack in trickle mode;
  adjust R20 on A3 if not. **§4-45A** (Errata #10): constant-current charge
  200–400 mA until ~31 V, then constant-voltage ~27 V trickle; discharge
  ~260 mA at 23 °C; individual cells accept 300–400 mA at 7.75 V max.
- **Change #7**: thermal fuse F2 (58 °C, 715110) on the oven module,
  interrupting +18.6 V to the oven heater and to latch Q6 (IN CAL goes out
  and stays out). Table 5-1: RT1 → RT3, RT4 (the oven thermistors are final
  assembly parts, as the A5 sheet's "OVEN" bracket suggests).
- **Change #5/#6**: A6 battery module rewired (spade-lug batteries, J10 power
  input connector 720854, W1/W2 leads, S1 BATTERY ON-OFF); rear-panel banana
  jacks replaced by a 3-pin external power connector J1 (plug 720847); Table
  2-2 item 6 text; Table 5-1 A6 651000 → 732628.
- Errata #1: Table 1-1 M07-200-601 → M07-200-603 (settles the note above);
  732A-7001 → 732A-7005 battery pack. Errata #6: Table 4-1 rheostat P/N
  484089 → 501601. Errata #7: acceptance test step 1c, line current < 0.35 A.

## Transcription QA (second round, by hand and by machine)

- `04-service-troubleshooting.md`: §4-44 all 26 steps, Table 4-2 and Table
  4-3 compared with PDF p38, p41, p42 — agree word for word (including the
  manual's own "A2" in step 12 and "CR27" in step 17, which the errata and
  the schematic show should read A3 and DS1/BTRY CHG). Figure 4-12 designator
  list: **"R19 — resistor, lower-center" is not on the page** (checked at
  600 dpi: the lower-left field prints R14, C5, R15, CR17, R13, R17, C6, TP1,
  RT1, R18, R20, R16, R12, CR14, Q4, CR22, Q5, Q6, CR21, R11, W1, TP5, CR20,
  CR26, TP2, CR16, CR13). R19 appears only from Rev F (errata Change #10).
  To be removed from the transcription.
- `tools/check_parts_ocr.py`: every six-digit stock number and five-digit
  manufacturer code in the three parts transcriptions agrees with the 600-dpi
  tesseract read wherever tesseract produced a parseable row (A3 73 of 82
  rows, A4 53 of 62, A5 71 of 102). The 22 reported differences are all
  tesseract glyph slips in the manufacturer part number (O for 0, Y for 4,
  S for 5, ~ for -, a stray = or ¥) or a mis-split designator (tesseract's
  "R6 1" for R61 on p62); none is a transcription error. Rows tesseract did
  not parse were read by two vision readers and adjudicated where they
  disagreed.
- **A3 R11.** Table 5-4: R11 RES, MTL. FILM, 12.7K ±1%, 1/8W (294918,
  CMF551272F). Schematic 732A-1003 prints R11 as 6.65K, 1/8W, 1% (beside
  CR22 at the Q5 base). The errata's Rev F charger schematic (Figure 12) does
  not letter R11. Caveat: value per parts list, schematic disagrees.
- `08-schematic-and-interconnect-notes.md` A3 section (P3 legend, test-point
  nets, printed values, NOTES and REF DESIG table) compared with my own
  reading of the 3x2 tiles: agrees.

## Transcription QA (third pass, 18 agents, every paragraph)

Corrections were few and small in the prose (a preserved typo restored, a
missing period, a heading's spacing) and larger in the figure descriptions:
the wiring described for Figures 4-6 to 4-10 (calibration hook-ups) was
rewritten from the drawings, the errata's Figures 9, 11 and 12 (A5 with the
A8 piggyback, A3 Rev F layout and charger schematic) had their callout lists
rebuilt, and Figure 3-1's block connections were corrected. In the parts
tables the only changes were the letter O for a digit 0 in six manufacturer
part numbers (Centralab `CW3COC224K` ×8 across A4/A5, Sprague `CO23B102E181M`),
settled by measuring glyph widths at 600 dpi — the same reading tesseract
gave. Every remaining `[unclear]` was confirmed illegible at 600 dpi (A3 R11's
wattage fraction, A4 C7's decimal point, hand-written wire flags on Figure
5-1). The abbreviations table (p70) was added as `07-abbreviations.md`.

## Designator positions (placement and review)

- Tesseract (four passes, `tools/ocr_designators.py`) placed about 40 % of the
  hand-lettered designators on each board and sheet; a vision model read every
  designator from gridded tiles (`tools/vlm_place.py plan`, 59 tiles for the
  three boards and their sheets, 30 for the two system figures, one agent per
  tile); `merge` snapped each reported point onto the lettering's connected
  components. Where the two readers disagreed by more than a box width the
  model's box won and the tier became `ambiguous`.
- Every placed marker was then rendered back onto the drawing eight to a
  sheet (`tools/review_markers.py`, 81 sheets for the boards, 24 for SYS) and
  judged by an independent agent per sheet; the verdicts went into the
  overrides as `confirm` (`tools/apply_review.py`). Found wrong: tesseract had
  snapped hardware designators that have no silkscreen (A3 F1, T1, FL1, H1, H2;
  A5 MP2, MP4, H1) onto other lettering, and had put A3 R17 on CR17 and A5 TP5
  on TP9, R6 on TP1, CR3 on Q3; Q4 (A3) and Q1, TP9 (A5) had oversized boxes.
  The hardware reads were dropped and the parts listed as not on the drawing;
  the rest were re-read by a targeted vision round and, where that read was
  still off (A5 R6, 35 px low), measured by hand on a gridded crop. A second
  render of the corrected markers was checked by eye.
- A5 TP5 is in the parts table and on the schematic but is not lettered on
  the 1983 drawing (it appears in the errata's Rev E layout); A4 CR4 has no
  lettering anywhere. Both are recorded as not on the drawing.
- Two labels the SYS reviewers flagged as "wrong" are intended: A3R20 sits on
  Figure 8-1's "R50" lettering (the drafting slip), A6S1 on the "BAT ON/OFF"
  function label (the figure gives the switch no designator). HR2–HR4 share
  the single "HR1-HR4" label; A5Q2 shares "Q1, Q2". Figure 8-1's oven-heater
  terminals E1/E2 are the motherboard's (A2E1/A2E2, per Figure 8-2), not A5's.
- Positions read once on the shared Figures 8-1 / 8-2 are copied to each
  board's `sh2` / `sh3` by `tools/share_interconnect.py` (A3 32, A4 29, A5 29
  items).

## Curated data (test points, procedures, symptoms, rails, caps)

Each dataset was written by one agent from the transcriptions and the 600 dpi
sheets, then checked by three others with different briefs — every number
against the page (citation), every circuit claim against the sheet
(circuit), and every field against the schema and the build (schema) — and
finally a cross-dataset pass reconciled the four. What that turned up, beyond
the disagreements already listed above:

- **Tolerances assumed where Table 4-3 prints none**: ±1.6 V (5 %) on the two
  32 V rows, ±0.5 V on 33.0 V, ±0.5 V on ≈18.5 V; the same three figures on
  the boards and on SYS, all marked inferred, all in the caveats.
- **A3 R1** reads "10M" in Table 5-4 and the errata but ".5" (0.5 Ω, the
  emitter resistor) on the sheet; caveat. **A3 T1 lead colours** on the
  transcription's E-terminal legend were corrected against the sheet (E2/E4
  are the ORN secondary leads).
- **A4 R4, R20, R13, R25, R26** values and ratings differ between Table 5-5 and
  the sheet (8.66 K vs 9.53 K, 8.2 K vs 6.81 K, …); caveat, measure the part.
- **A3 TP5** is on Q6's base lead, and A5's TP11/TP12 chain feeds the 1.018 V
  tap (E34), TP13/TP14 the 1 V tap (E35) — both corrected in these notes and
  in the schematic-notes transcription after the circuit lens traced them.
- The A3 charger's control-side routing (thermistor and BTRY CHG LED wiring)
  was resolved at 600 dpi and its caveat rewritten to say what was read.
- SYS's *Signal map* table (37 rows) traces every inter-board signal through
  A3 P3 → A2 J3 → A2 J2 → A4 P2 → the A5 E-terminals, with the test points on
  each net; 92 SYS links to board designators all resolve.

## How the parts tables write a value (found while auditing the capacitors)

Table 5-4/5-5/5-6 punctuate differently from the 5700A's lists the engine was
written against, and every difference silently cost a parsed value. All four
were read on the page image (PDF p54, p58) before anything was changed:

- **"CAP, ELECT, …"** is how the 732A names an aluminium can — A3 C1
  (100 UF +75/-20%, 80V), A3 C3 (330 UF -20/+75%, 80V) and A4 C1
  (330 UF +75/-20%, 80V), the three reservoirs in the instrument. The 5700A's
  lists write "CAP, AL", so the audit classified these as family `ELECT`: no
  ESR limit, no drying-out verdict, and no row under Aluminium in the rework
  round. `Caps.type` now maps ELECT (and ELEC, ALUM) onto AL.
- **Tolerance is written "+/-20%", not "+-20%"**, and lives in the same
  comma-field as the value ("0.1 UF +/-20%"). The value parser split only on
  "+-", so *every* capacitor and resistor description in all three tables
  failed to yield a value. `Parts.spec` now splits on "+/-" as well.
- **The asymmetric pair is slashed and prints in either order**: "+75/-20%"
  (A3 C1, A4 C1) and "-20/+75%" (A3 C3) are the same tolerance, so the sign
  decides which limit is which, not the position.
- **A full stop stands in for a comma** in "CAP, CER. 0.22 UF" (A4 C10) and
  "RES, MTL. FILM", so a stop that ends a word is a field break too; digits
  after a stop ("0.22") are untouched. **"50DCV"** (A5 C10) is the rating
  suffix written backwards and now reads as 50 V.

One row is left unparsed on purpose: **A3 C9 and C10** print "CAP, CER, 0.05
+/-20%, 50V" — no unit, confirmed on the page image and in the 600 dpi read.
0.05 µF is the only sensible reading, but the table does not say so, so the
transcription stands and the caveat is a note on the part (extras `amend`).

## Which resistors are a rework family (read off the tables)

The *Rework* round replaces carbon composition and nothing else. The families
were taken from the description's second field in Tables 5-4, 5-5 and 5-6 and
counted:

| Family | A3 | A4 | A5 | |
|---|---|---|---|---|
| `RES, COMP` carbon composition | 5 | 18 | 20 | the round; drifts up with age and moisture |
| `RES, MTL. FILM` metal film | 9 | 5 | 9 | stable |
| `RES, WW` wirewound | 1 | 1 | 21 | stable |
| `RES, CF` carbon film | 1 | — | — | A3 R19, added by errata Change #10; film on ceramic, stable |
| `RES, DEP. CAR` deposited carbon | — | 1 | 1 | same construction, older name |
| `RES, VAR` / `VAR, CERMET` | 2 | 1 | 3 | pots |
| sets (`MATCHED RESISTOR SET`, `REF AMP SET`, …) | — | — | 10 | no single value to measure |

Two more carbon comps live outside the three boards and are on the SYS list:
the front panel's R1 (2.7 Ω 1 W, Table 5-1, in series with C1 across 10V
HI/LO) and the battery board's A6 R1 (51 kΩ, Table 5-7). Forty-five in all.

Six of A5's twenty are starred in Table 5-6 — R24, R25, R26, R62, R63, R64 —
i.e. inside the reference §4-53 says is not field repairable. They are listed
and marked, and no bulk tick selects them.

The interconnect view letters the boards' own parts with an assembly prefix
(SYS `A3R3` links to A3 `R3`), so a round that walks every dataset saw 54
where there are 45. `BoardExplorer.mirrors()` is the test that drops them; the
capacitor round had the same latent double-count.
