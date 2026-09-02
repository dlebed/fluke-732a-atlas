# Section 8 schematic annotations (hand-lettered sheets)

Transcription of the lettering printed on the Section 8 schematic figures of the Fluke 732A manual (732A-1301, -1001, -1002, -1003, -1004, -1005, -1006, -1007). Everything below is read from the 600 dpi scans; the parts lists do not carry these annotations. Component *values* are given exactly as lettered on the sheet (the sheets write ohms as a small "Ω"/"~" glyph after the number, e.g. "24.3Ω MF"; capacitances are in microfarads unless "pf" is lettered). Anything not read with confidence is marked `[unclear: ...]`.

Geometry conventions used below: "A → B" means a printed wire runs from A to B; "(tied)" means two connector pins are strapped together on the sheet.

---

## Figure 8-1. Interconnect Diagram (PDF p85, manual p8-3) — drawing 732A-1301

Sheet layout (left to right): the A3 PRE-REGULATOR & BATTERY CHARGING block (top left) with the A6 BATTERY PACK below it; the OVEN HEATER box and OVEN HEATER DRIVER / REGULATOR (dashed) sub-blocks of the A4 REFERENCE SERIES PASS ELEMENT in the middle; the A5 REFERENCE & OVEN CONTROL block on the right; the FRONT PANEL strip at the far right. Block titles as lettered: "A-3 PRE-REGULATOR & BATTERY CHARGING", "A6 BATTERY PACK", "A4 REFERENCE SERIES PASS ELEMENT", "OVEN HEATER", "OVEN HEATER DRIVER", "REGULATOR", "A5 REFERENCE & OVEN CONTROL", "FRONT PANEL". The handwritten "A-3", "A6", "A4", "A5" designators are in script. Drawing number "732A-1301" at lower right.

### A3 block — P3 / J3 pin legend (A3 P3 mates to A2 J3)

| A3 P3 pin | printed on Fig 8-1 | goes to |
|---|---|---|
| 1 | SHIELD | ground symbol on the J3 side |
| 6 | NC (strapped to pin 1 on the P3 side) | — |
| 2 | (+RAW; TP6 sits on this line, after R1) | A4 J2/P2 pins 13, 14 |
| 8 | (–RAW) | A4 J2/P2 pins 23, 24 |
| 4 | → 12 | TO FRONT PANEL (AC PWR LED +) |
| 7 | → 13 | TO FRONT PANEL (AC PWR LED –) |
| 9 | (+ battery, CR16 / CR13 line) | A4 J2/P2 pin 15, A6 J4/P4 pin 1 |
| 10 | (+ battery; strapped to 9 on both sides of the connector) | — |
| 13 | → 17 | TO FRONT PANEL (BTRY CHG LED +) |
| 14 | → 18 | TO FRONT PANEL (BTRY CHG LED –) |
| 17 | (– battery; TP1 sits on this line) | A4 J2/P2 pins 21, 22; A6 J4/P4 pin 2 (–) |
| 18 | (– battery; strapped to 17 on both sides of the connector) | — |
| 16 | thermistor | A6 J4/P4 pin 6 (RT2) |
| 15 | thermistor | A6 J4/P4 pin 5 (RT2) |
| 11 | thermistor | A6 J4/P4 pin 3 (RT1) |
| 12 | thermistor | A6 J4/P4 pin 4 (RT1) |

Lettered at the bottom of the P3/J3 column: "P3 / J3" with pins "16 15 11 12" running down to "J4 / P4" pins "6 5 3 4"; RT2 is drawn across P4 pins 6-5 and RT1 across P4 pins 3-4. J4/P4 pin "2 –" and pin "1 +" carry the battery pack. A switch lettered "BAT ON/OFF" is in series with the "+" (pin 1) lead.

### A3 block — designators appearing on Fig 8-1

Transformer block lettered "TRANSFORMER" fed from a 3-pin line plug with chassis-ground symbol; TP3; bridge rectifier (4 unlabelled diodes); two unlabelled diodes between transformer secondary and bridge; R9; CR25; CR19; Q1; R1; TP6; CR7; CR6; CR12; "AC PWR (FR PNL)" LED (dashed, off-board); TP4; R3; Q2; CR13; R4; CR20; Q6; CR16; R16; R17 (with an unlabelled thermistor symbol beside it); R50 (pot); TP5; unlabelled diode below R4; TP2; W1 (jumper, drawn as a pair of open circles); R11; "BTRY CHG (FR PNL)" LED (dashed, off-board); Q3; Q4; R12; R13; R10 (pot); unlabelled zener below R10; unlabelled diode beside Q3; unlabelled diode and unlabelled zener on the left rail beside R12; TP1.

Test points, A3 on Fig 8-1: TP1 on the – battery bus (P3 pins 17/18); TP2 on the node between the W1 jumper and R11; TP3 on the bridge-rectifier + output; TP4 on the return line below the bridge (the –RAW line to P3 pin 8); TP5 at the Q6 base-lead node (R16 / R17 / thermistor); TP6 on the +RAW line between R1 and P3 pin 2.

### A6 BATTERY PACK — parts drawn

BLK terminal and RED terminal (rear-panel power input, drawn as circles); CR1 (diode) and R1 (resistor) in parallel between the BLK terminal line and the – bus (J4/P4 pin 2); J1, J2, J3, J4 (battery connectors, each drawn as a rectangle over its battery); BT1, BT2, BT3, BT4 (batteries, in series); DS1 drawn as a lamp (circle with zig-zag) between the RED terminal line and the J4 (+) end / BAT ON/OFF switch. J4/P4 pins "2 –" and "1 +" go up to the A3 block; the "BAT ON/OFF" switch is in the "+" lead.

### OVEN HEATER box (between A3 and A4)

"E1" terminal, "BLK (4 WIRES)" → heater element lettered "HR1-HR4" → "WHT (4 WIRES)" → "E2" terminal. E1 runs down to A4 J2/P2 pin 11; E2 runs to A4 P2/J2 pin 1.

### A4 block — J2 / P2 pin legend on Fig 8-1

Left side of A4 ("J2 P2", mating the A2 mother board):

| A4 P2 pin | Fig 8-1 lettering / connection |
|---|---|
| 11 | from OVEN HEATER E1 (BLK) |
| 12 | NC (drawn on the 18.6V line; TP1 on this line) |
| 13 | tied to 14, from A3 P3 pin 2 (+RAW) |
| 14 | (+RAW) |
| 15 | from A3 P3 pin 9/10 (+ battery); unlabelled diode from 15 to the 18.6V line |
| 21 | tied to 22 |
| 22 | from A3 P3 pin 17 (– battery) |
| 23 | tied to 24 |
| 24 | from A3 P3 pin 8 (–RAW); TP3 on this line |

Right side of A4 ("P2 J2", top) and the front-panel / A5 harness numbers printed beside them:

| A4 P2 pin | harness no. | destination as lettered |
|---|---|---|
| 1 | (to OVEN HEATER E2, WHT 4 WIRES) | — |
| 26 | 10 | A5 E10 (BLK) |
| 27 | 11 | A5 E11 (BRN) |
| 2 | 1 | A5 E1 (BRN) — "BUFFER AMP/DRIVER AMP COMMON" |
| 10 | 8 | A5 E8 (GRA) — lettered "18.6V" |
| 16 | 9 | A5 E9 (WHT) |
| 18 | 14 | TO FRONT PANEL (IN CAL LED +) |
| 20 | 16 | TO FRONT PANEL (IN CAL LED –); "IN CAL (FR PNL)" LED drawn dashed |
| 19 | 15 | TO FRONT PANEL (RESET) |
| 3 | 2 | A5 E2 (RED); the line leaves the TP2 common node |
| 4 | 3 | A5 E3 (ORN) |
| 5 | NC | — |
| 6 | 4 YEL | TO SERIES PASS ELEMENT |
| 7 | 5 GRN | TO SERIES PASS ELEMENT |
| 8 | 6 BLU | TO SERIES PASS ELEMENT |
| 9 | 7 VIO | TO SERIES PASS ELEMENT |

Voltages lettered in A4: "18.6V" on the horizontal supply line running from the J2/P2 12/13 area across the top of the regulator (TP1 sits on it).

### A4 block — designators appearing on Fig 8-1

OVEN HEATER DRIVER: Q14, R24, R25, Q13, R26. Main area: TP1, CR2, Q2, Q1, R4, R22 (arrow / pot symbol), two unlabelled diodes below R22, R7, R8, R9, Q3, Q4, Q8, CR14, unlabelled resistor + transistor at top right, "LATCH CKT Q6 Q7" (box), TP2, TP3, unlabelled diode between pin 15 and the 18.6V line. REGULATOR (dashed): R1, Q12, R3, R2, R21, CR13.

Test points, A4 on Fig 8-1: TP1 on the 18.6V line (P2 pins 12/13 node); TP2 on the common rail feeding P2 pins 3 and 4; TP3 on the – rail at P2 pin 24 / Q4 emitter.

### A5 block — E-terminal legend on Fig 8-1

Left edge (from A4 / mother board, wire colour lettered beside each):

| E | colour | lettering / net |
|---|---|---|
| E1 | BRN | BUFFER AMP/DRIVER AMP COMMON |
| E9 | WHT | top of the U5 bridge (RT3/RT4 network) |
| E10 | BLK | U5 output line |
| E11 | BRN | line lettered "18.6V" beside U5 (U5 supply) |
| E2 | RED | bottom of the U5 bridge |
| E8 | GRA | "18.6V" — feeds CR5 / CR2 / SERIES PASS ELEMENT |
| E3 | ORN | common (bottom rail) |

Right edge (to FRONT PANEL):

| E | lettering |
|---|---|
| E23 | from SERIES PASS ELEMENT J2-6 output node |
| E24 | strapped to E23/E25 bus |
| E25 | strapped bus |
| E33 | 10V HI |
| E34 | 1.018V HI |
| E35 | 1V HI |
| E36 | LO |
| E26 | strapped to E36/E27/E28 (LO bus) |
| E27 | LO bus |
| E28 | LO bus |
| E22 | GRA → OVEN TEMP THMS (front panel) — RT2 across E22/E21 |
| E21 | GRA → OVEN TEMP THMS (front panel) |

Lettered inside A5: "BUFFER AMP/DRIVER AMP COMMON"; "18.6V" (twice: on E8 and on the E11 line beside U5); "U5"; "RT3 / RT4 } SENSES TEMP OF HR1–HR4 OVEN HEATERS" (four unlabelled resistors form the bridge around RT3/RT4); "CR5"; "CR2"; "(SEL)" resistor; "U2" (transistor + zener in one outline); "U1" (op-amp, + and – inputs); "R2"; "R3"; a box lettered "A4 Q12 / SERIES PASS ELEMENT / J2 6 / J2 7 8 9" with harness numbers "4" (from J2-6) and "5 6 7" (from J2-7, 8, 9); a box lettered "SERIES PASS DRIVE TRANSISTORS / A5 Q1, Q2"; pots lettered "1.018V ADJ", "1V ADJ", "10V ADJ" with unlabelled fixed resistors in the divider; "RT2".

A5 designators appearing on Fig 8-1: U5, RT3, RT4, CR5, CR2, U2, U1, R2, R3, Q1, Q2 (in the drive-transistor box), RT2, plus the "(SEL)" resistor and the three ADJ pots (no R numbers printed on this sheet).

### FRONT PANEL strip (right edge)

| terminal / no. | colour | lettering |
|---|---|---|
| GUARD | BLU | (guard symbol) |
| GROUND | GRN/YEL | (chassis-ground symbol) |
| 12 | RED | AC PWR LED + } DS1 |
| 13 | ORN | AC PWR LED – } DS1 — bracket "TO PRE-REG & BTRY CHG" |
| 17 | VIO | BTRY CHG LED + } DS2 |
| 18 | GRA | BTRY CHG LED – } DS2 |
| 14 | YEL | IN CAL LED + } DS3 — bracket "TO REGULATOR" |
| 16 | BLU | IN CAL LED – } DS3 |
| 15 | GRN | RESET |
| — | — | 10V HI (from E33) |
| — | — | 1.018V HI (from E34) |
| — | — | 1V HI (from E35) |
| — | — | LO (from E36) |
| — | GRA | OVEN TEMP THMS (from E22) |
| — | GRA | OVEN TEMP THMS (from E21) |

---

## Figure 8-2. A1 LED, A2 Mother Board and A6 Battery Module PCB Assemblies — board outlines (PDF p86, manual p8-4)

Three component-side outlines, no schematic lettering other than designators:

- **A1 LED, 732A-1606**: tall rectangle with three boxes lettered "DS1", "DS2", "DS3" (top to bottom).
- **A2 Mother Board, 732A-1605**: outline with a step notch at each upper corner; connectors lettered "J3" (small, upper left; two more unlabelled edge connectors of the same style below it), "J2" (long vertical connector in the centre, plus a small unlabelled one below it), "J4" (upper right); test points "TP1" and "TP2" lettered along the top edge.
- **A6 Battery Module, 732A-1604**: long strip; "P4" at the left end (edge-connector fingers); "J1", "J2", "J3", "J4" (battery holders); "DS1" (long rectangle, lamp); "CR1" (diode outline); "R1"; "RT2" and "RT1" (small squares).

Figure caption: "Figure 8-2. A1 LED, A2 Mother Board and A6 Battery Module PCB Assemblies".

---

## Figure 8-2 (cont). A1 LED, A2 Mother Board and A6 Battery Module schematic (PDF p87, manual p8-5) — drawings 732A-1004, -1005, -1006

Dashed outlines: "MOTHER PCB 732A-1005" (large, left/centre), "BATTERY PCB 732A-1004" (upper right), "732A-1006 LED PCB" (lower right). Brackets: "REAR PANEL" (battery on-off switch and power input), "FRONT PANEL" (LED PCB and RESET).

### OVEN heaters (top centre, bracket "OVEN")

| designator | printed value |
|---|---|
| HR1 | 110Ω |
| HR2 | 110Ω |
| HR3 | 440Ω |
| HR4 | 440Ω |

All four heaters are drawn in parallel: the four left ends are tied to one vertical (dots at HR2, HR3, HR4), the right ends of HR1/HR2 are joined and run across to the joined right ends of HR3/HR4; the two verticals go down as wires lettered "WHT" (left, to E1) and "BLK" (right, to E2). E1 is also tied to J2 pin 11 and carries test point "TP1"; E2 carries "TP2" and reaches J2 pin 1 through a dashed two-circle jumper symbol. [transcriber note: Figure 8-1 letters the E1 heater wires "BLK (4 WIRES)" and the E2 wires "WHT (4 WIRES)", the opposite of the WHT/BLK lettering on this sheet.]

### A2 mother board J3 (mates A3 P3)

| J3 pin | connection on the sheet |
|---|---|
| 9 | tied to 10; runs right to J4/P4 pin 1 (+, E4) and (via a vertical) to J2 pin 15 |
| 10 | tied to 9 |
| 17 | tied to 18; runs right to J4/P4 pin 2 (–) and (via a vertical) to J2 pins 21 and 22 |
| 18 | tied to 17 |
| 11 | → J4/P4 pin 3 |
| 12 | → J4/P4 pin 4 |
| 15 | → J4/P4 pin 5 |
| 16 | → J4/P4 pin 6 |
| 1 | "COMMON (GUARD BOX)" — ground symbol |
| 5 | NC |
| 6 | NC |
| 4 | → 12 RED (W2, LED PCB) |
| 13 | → 17 VIO (W2, LED PCB) |
| 14 | → 18 GRA (W2, LED PCB) |
| 7 | → 13 ORN (W2, LED PCB); tied to 8 |
| 8 | tied to 7; runs right to J2 pin 24 (23 tied) |
| 3 | runs right to J2 pin 17 |
| 2 | runs right to J2 pin 13 (14 tied) |

### A6 battery PCB J4 / P4

| J4/P4 pin | connection |
|---|---|
| 1 | → E4 (+); E4 runs up and across to the BATTERY ON-OFF switch, whose other side is E3 (+) at the BT4 (+) end of the string |
| 2 | – bus: bottom of the string at BT1 (J1) and the CR1 / R1 node |
| 3 | RT1 one end |
| 4 | RT1 other end — "RT1 10K 25°C" |
| 5 | RT2 one end |
| 6 | RT2 other end — "RT2 10K 25°C" |

Battery PCB parts: BT1, BT2, BT3, BT4 (each with – and + marked, in series through J1, J2, J3, J4); "R1 51K" in parallel with "CR1" between the – bus and the E2 line; "DS1" (drawn as a neon-lamp circle) between the E1 line and the E3 line; E4 (+), E3 (+) → "BATTERY ON-OFF" switch (rear panel), E1 (+) → RED terminal, E2 (–) → BLK terminal.

Rear-panel text: "BATTERY ON-OFF"; "POWER INPUT / 24-40V DC / 24-30V AC, 50-60 Hz, 0.5A"; RED (+), BLK (–).

CAUTION block (verbatim):
> CAUTION
> TO PREVENT INSTRUMENT DAMAGE DO NOT CONNECT POWER INPUT TERMINALS TO FRONT PANEL TERMINALS OF SAME UNIT. USE FLOATING SOURCE ONLY.

### A2 mother board J2 (mates A4 P2)

| J2 pin | connection |
|---|---|
| 22 | – battery vertical (from J3 17/18 line) |
| 21 | – battery vertical (from J3 17/18 line) |
| 15 | + battery vertical (from J3 9/10 line) |
| 1 | E2 (BLK heater wire) via dashed jumper symbol |
| 11 | E1 (WHT heater wire) |
| 5 | NC |
| 18 | ← YEL 14 (W2) |
| 12 | NC |
| 19 | ← GRN 15 (W2) |
| 25 | NC |
| 20 | ← BLU 16 (W2); also strapped down to the ORN 3 / pin 4 node |
| 23 | tied to 24 |
| 24 | from J3 pin 8 |
| 17 | from J3 pin 3 |
| 13 | from J3 pin 2; tied to 14 |
| 14 | tied to 13 |
| 4 | ← ORN 3 (W1) |
| 2 | ← BRN 1 (W1) |
| 3 | ← RED 2 (W1) |
| 6 | ← YEL 4 (W1) |
| 7 | ← GRN 5 (W1) |
| 8 | ← BLU 6 (W1) |
| 9 | ← VIO 7 (W1) |
| 10 | ← GRA 8 (W1) |
| 16 | ← WHT 9 (W1) |
| 26 | ← BLK 10 (W1) |
| 27 | ← BRN 11 (W1) |

### W1 harness — "TO REFERENCE PCB 732A-1001"

| E (reference PCB) | colour | W1 no. | J2 pin |
|---|---|---|---|
| E1 | BRN | 1 | 2 |
| E2 | RED | 2 | 3 |
| E3 | ORN | 3 | 4 |
| E4 | YEL | 4 | 6 |
| E5 | GRN | 5 | 7 |
| E6 | BLU | 6 | 8 |
| E7 | VIO | 7 | 9 |
| E8 | GRA | 8 | 10 |
| E9 | WHT | 9 | 16 |
| E10 | BLK | 10 | 26 |
| E11 | BRN | 11 | 27 |

### W2 harness and 732A-1006 LED PCB (bracket "FRONT PANEL")

| LED PCB terminal | colour | source | function |
|---|---|---|---|
| 13 (square pad) | ORN | J3-7 | DS1 anode side — "AC POWER" |
| 12 | RED | J3-4 | DS1 |
| 18 (square pad) | GRA | J3-14 | DS2 — "BATTERY CHG" |
| 17 | VIO | J3-13 | DS2 |
| 16 (square pad) | BLU | J2-20 | DS3 — "IN CAL" |
| 14 | YEL | J2-18 | DS3 |
| 15 | GRN | J2-19 | "RESET" pushbutton (solid circle) |

DS1, DS2, DS3 are each drawn as two LEDs (anti-parallel pair in one outline) with the light-emission arrows.

### NOTES (verbatim)
> NOTES: UNLESS OTHERWISE SPECIFIED:
> 1. ALL RESISTORS ARE 1/4 W, 5%.

Drawing numbers lettered at lower right: "732A-1004 / -1005 / -1006". Caption: "Figure 8-2. A1 LED, A2 Mother Board and A6 Battery Module PCB Assemblies (cont)".

---

## Figure 8-3. A3 Pre-Regulator PCB Assembly (cont) — schematic (PDF p89, manual p8-7) — drawing 732A-1003

Dashed outline lettered "PRE-REGULATOR PCB". Off-board on the left: transformer "T1", fuse "F1", line filter "FL1", line connector "J1".

### Line input (off-board)

- "J1" (3-pin, lettered N, G, L) — "100-132V AC / 200-264V AC / 50-60 Hz / 30 VA".
- "FL1" (dashed box: two inductors lettered "L", three capacitors); "CHASSIS" ground symbols; "GRN/YEL" ground lead to chassis.
- "F1" with "100-132V 3/8A SB / 200-264V 3/16A SB".
- Wires from J1/FL1: "BLK" (line), "WHT" (neutral), "GRN/YEL" (ground).
- T1 windings and lead colours: two primaries and two secondaries with dots; leads "GRA", "WHT", "VIO", "BLU", "BRN", "YEL", "BLK", "ORN", "ORN", "GRN" (GRN is the lead from the dashed shield beside the core, to E12 SHIELD #1; the core itself goes to E14 CORE); three dashed shield lines.

### E-terminal legend (A3 board edge, left)

| E | lettering |
|---|---|
| E1 | SHIELD #2 |
| E2 | AC SECONDARY |
| E3 | SHIELD #3 |
| E4 | AC SECONDARY |
| E11 | 1ST PRIMARY |
| E10 | 1ST PRIMARY (dot) |
| E7 | LINE #1 |
| E8 | CHASSIS GROUND |
| E9 | LINE #2 |
| E6 | 2ND PRIMARY |
| E5 | 2ND PRIMARY (dot) |
| E16 | 2ND TAP |
| E12 | SHIELD #1 |
| E13 | (jumper post) |
| E14 | CORE — "JUMPER SELECT IN TEST" (dashed jumper from E14 to E13 or E15) |
| E15 | GUARD |

### Line-voltage switches

- "S1" (dashed box, 2-pole): positions lettered "220-240V" and "100-120V".
- "S2" (dashed box, 2-pole): positions lettered "100-220V" and "120-240V".

### P3 pin legend (right edge)

| P3 pin | printed net |
|---|---|
| 1 | GUARD BOX |
| 2 | + RAW (TP6 on this line, after "R1 .5") |
| 3 | SWITCH CONTROL |
| 6 | GUARD (strapped to pin 1) |
| 5 | NC |
| 4 | + } AC POWER LED |
| 7 | – } AC POWER LED (strapped to pin 8 on the board side) |
| 8 | – RAW |
| 11 | THERMISTOR (the W1 lower-circle line; TP2 sits on it) |
| 9 | + } + BATTERY |
| 10 | (strapped to 9, right of CR13 / CR16) } + BATTERY |
| 13 | + } BATTERY CHARGE LED |
| 14 | – } BATTERY CHARGE LED |
| 12 | THERMISTOR |
| 15 | } THERMISTOR VOLTAGE COMPENSATION |
| 16 | } THERMISTOR VOLTAGE COMPENSATION |
| 17 | } – BATTERY (TP1 on this line) |
| 18 | } – BATTERY (tied to 17) |

### Test points (Fig 8-3)

| TP | where it sits |
|---|---|
| TP1 | – BATTERY bus (P3 pins 17/18, bottom of R14 / R10 / C5 chain) |
| TP2 | on the vertical running from the CR26 / CR14 junction down to R11, at its crossing with the W1 lower-circle line (P3 pin 11 THERMISTOR) |
| TP3 | + output of bridge CR1 (C1 / CR25 / CR19 node) |
| TP4 | return line from the bridge CR1 (–) joining C1 (–), C2 (top) and the C3 (–) end; the parallel line below it (CR2 / CR3 cathodes, C3 +, C2 bottom) feeds the R4 / R3 left ends |
| TP5 | Q6 base-lead node (CR28 / RT1 / R16 / R17) |
| TP6 | + RAW line at P3 pin 2 (right of R1) |

W1: jumper (two open circles); upper circle on the line from the R3 3.3Ω right end / Q2 collector, which continues right through CR13 to the + BATTERY pins 9/10, lower circle on the TP2 / P3 pin 11 THERMISTOR line.

### Component values printed on Fig 8-3

| designator | printed value |
|---|---|
| R1 | .5 |
| R3 | 3.3, 1/2W, 5% |
| R4 | 1.54K, 1/8W, 1% |
| R6 | 510 |
| R7 | 22.6, 1/8W, 1% |
| R8 | 4.02K, 1/8W, 1% |
| R9 | 10K, 1/2W, 5% |
| R10 | 500 (pot) |
| R11 | 6.65K, 1/2W, 1% [unclear: wattage lettered "½w" — could be 1/8W] |
| R12 | 16.2K, 1/8W, 1% |
| R13 | 33.2K, 1/8W, 1% |
| R14 | 17.4K, 1/8W, 1% |
| R15 | 10K |
| R16 | 10K |
| R17 | 6.49K |
| R18 | 43.2K |
| R20 | 50K (pot) |
| RT1 | 10K |
| C1 | 100 |
| C2 | .1 |
| C3 | 330 (polarised, + marked) |
| C4 | 4700 pf |
| C5 | 1 (polarised, + marked) |
| C6 | .01 |
| C9 | .05 |
| C10 | .05 |
| CR1 | bridge rectifier (+ and – marked) |
| CR2, CR3, CR5, CR7, CR8, CR9, CR13, CR16, CR18, CR19, CR23 | diodes, plain bar (no value lettered) |
| CR6, CR11, CR20, CR21, CR22, CR24, CR25, CR26, CR28 | diodes drawn with an I-shaped bar (short strokes at both ends of the bar; no value lettered) |
| CR4, CR10, CR12, CR14, CR15 | zener symbols (Z-bent bar; no value lettered) |
| Q1, Q2, Q3, Q4, Q5, Q6 | transistors (no type lettered) |
| DS1 | LED (on-board) |
| S1, S2 | line-voltage switches |
| T1, F1, FL1, J1 | off-board (values above) |

R2, R5 and R19 do not appear on the sheet (R19 is in the NOT USED column).

### NOTES (verbatim)
> NOTES: UNLESS OTHERWISE SPECIFIED
> 1. ALL RESISTANCES ARE IN OHMS AND ALL CAPACITANCE ARE IN MICROFARADS
> 2. ALL RESISTORS ARE 1/4 W 5% CC.

### REF. DESIG. table (verbatim)

| LAST USED | NOT USED |
|---|---|
| R20 | R19 |
| C10 | C7, 8 |
| CR28 | CR27, 17 |
| Q6 | |
| S2 | |
| DS1 | |

Drawing number "732A-1003". Caption: "Figure 8-3. A3 Pre-Regulator PCB Assembly (cont)".

---

## Figure 8-4. A4 Regulator PCB Assembly (cont) — schematic (PDF p91, manual p8-9) — drawing 732A-1002

### P2 pin legend — left column

| P2 pin | printed net |
|---|---|
| 6 | } REF SUPPLY (R3 24.3Ω MF) |
| 7 | } REF SUPPLY (Q12 emitter / R1) |
| 8 | } REF SUPPLY (Q12 base / R2) |
| 9 | } REF SUPPLY (CR13 / R21) |
| 12 | NC (on the +RAW bus) |
| 13 | } + RAW |
| 14 | } + RAW |
| 15 | + BATTERY (CR15 to +RAW bus) |
| 17 | NC |
| 21 | } – BATTERY |
| 22 | } – BATTERY |
| 23 | } – RAW |
| 24 | } – RAW |
| 25 | NC |
| 26 | HEAT DRIVE (R26 / Q13 line) |
| 27 | – 2 V |

### P2 pin legend — right column

| P2 pin | printed net |
|---|---|
| 10 | + TEMP REG (strapped to 11 on the board side) |
| 11 | + HEATER (strapped to 10) |
| 16 | + BRIDGE |
| 18 | IN CAL LED |
| 20 | COMMON |
| 19 | RESET |
| 1 | HEATER |
| 2 | – TEMP. REG |
| 3 | – BRIDGE |
| 4 | – REF |
| 5 | GUARD BOX FRONT PANEL |

Pins 2, 3, 4, 5 are strapped together to the "COMMON" node (ground symbol) which also carries "TP2".

### Test points (Fig 8-4)

| TP | where it sits |
|---|---|
| TP1 | REF SUPPLY output node — right end of R1 (348Ω) / R2 / R21 junction, feeding the CR2 line |
| TP2 | COMMON (ground symbol; P2 pins 2-5) |
| TP3 | – BATTERY / – RAW bus (below C1, P2 pins 21-24) |

### Component values printed on Fig 8-4

| designator | printed value |
|---|---|
| R1 | 348Ω MF, 1/8W, 1% |
| R2 | 1.21K MF, 1/8W, 1% |
| R3 | 24.3Ω MF, 1/8W, 1% |
| R4 | 9.53K, 1/8W, 1% |
| R5 | 3K |
| R6 | 4.3K |
| R7 | 18K |
| R8 | 91K (the rounded 9 matches the 9 of the "R9" designator; the 5 of R15 "51K" is angular) |
| R9 | 91K |
| R10 | 5K |
| R11 | 10K |
| R12 | .39, 2W, 5% |
| R13 | 2.7, 1/2W, 5% |
| R14 | 150K |
| R15 | 51K |
| R16 | 1M |
| R17 | 2.7K |
| R18 | 16K, 1/2W, 5% |
| R19 | 18K, 1/2W, 5% |
| R20 | 6.81K, 1/8W, 1% |
| R21 | 1K |
| R22 | 5K (pot, arrow from R6) |
| R23 | 270K |
| R24 | 1K |
| R25 | 51K, 1/2W, 5% |
| R26 | 10, 1/2W |
| C1 | 330/80V (polarised, + marked) |
| C2 | 82 (polarised, + marked) |
| C3 | 10 (polarised) |
| C4 | 10 (polarised) |
| C5 | .22 |
| C6 | .047 |
| C7 | .01 [unclear: lettered "01" with the point faint] |
| C8 | .22 |
| C9 | 22 (polarised, + marked) |
| C10 | .22 |
| CR1, CR2, CR9 | zener/reference symbols drawn inside a circle (no value lettered) |
| CR3, CR5, CR6, CR7, CR8 | diodes, plain bar |
| CR10, CR12, CR13, CR14 | diodes drawn with an I-shaped bar (short strokes at both ends of the bar) |
| CR15 | diode whose bar ends are bent toward the triangle |
| Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q12, Q13, Q14 | transistors (no type lettered) |
| DS1 | LED (on-board) |

### NOTES (verbatim)
> NOTES: UNLESS OTHERWISE SPECIFIED:
> 1. ALL RESISTANCES ARE IN OHMS AND ALL CAPACITANCE ARE IN MICROFARADS.
> 2. ALL RESISTORS ARE 1/4 W 5% CC.

### REF. DES table (verbatim)

| LAST USED | NOT USED |
|---|---|
| R26 | |
| C10 | |
| CR-15 | CR4, 5, 11 |
| Q14 | Q9-11 |
| DS1 | |

Note: "CR5" is nevertheless lettered on the sheet (diode in series with R4 9.53K from the +TEMP REG line), although the table lists CR5 as NOT USED — [transcriber note: table vs. drawing inconsistency in the original].

Drawing number "732A-1002". Caption: "Figure 8-4. A4 Regulator PCB Assembly (cont)".

---

## Figure 8-5. A5 Reference PCB Assembly (cont) — schematic (PDF p93, manual p8-11) — drawings 732A-1001, -1007

Dashed outlines: "732A-1001 REFERENCE PCB" (main), "732A-1007 CAL PCB" (bottom centre), "TERM STRIP INSIDE FRT PAN." (right), bracket "OVEN" over RT4 and RT3 (top left), bracket "FRONT PANEL" (far right). Left bracket "TO MOTHER PCB 732A-1005".

### E-terminal legend — left edge (to mother PCB, wire colours)

| E | colour |
|---|---|
| E9 | WHT (top rail; TP6 on it; RT4, RT3, R21, R27, R42/U4 supply hang from it) |
| E2 | RED (return rail of the thermistor bridge: C6, RT1, C7, R29, C5) |
| E1 | BRN (U3 pin 4 supply return) |
| E11 | BRN |
| E10 | BLK |
| E8 | GRA (line ends at the CR5 anode / R9 top node) |
| E4 | YEL (rail carrying CR6 (to ground), the Q2 upper leg, the U1 pin-7 line and R62; beyond R62 it steps up and reaches the R63 / E23 10V HI node) |
| E5 | GRN (Q2 base and the Q1 upper leg) |
| E7 | VIO (Q1 base, the Q2 lower leg and CR1) |
| E6 | BLU (Q1 lower leg) |
| E3 | ORN (bottom common rail) |

### E-terminal legend — right edge (to FRONT PANEL / term strip)

| E | lettering |
|---|---|
| E33 | 10V HI |
| E34 | 1.018V HI |
| E35 | 1V HI |
| E36 | LO |
| E23 | 10V HI |
| E22 | THERMISTOR (RT2 / R43 / C1 node) |
| E21 | THERMISTOR (other end of RT2) |
| E24 | 10V HI |
| E25 | 10V HI (into the term strip) |
| E26 | LO (into the term strip) |
| E27 | LO |
| E28 | LO |

### Oven thermistors and thermistor bridge

- "RT4 10K, 25°C" and "RT3 10K, 25°C" (bracket "OVEN").
- "RT1 10K 25°C" (on board, between the R22 left node and the E2 rail).
- "RT2 10K 25°C" between E22 and E21; "R43 100K" and "C1 .22" from E22 to ground symbol.

### Term strip inside front panel (off-board)

Between the E25 line ("10V HI") and the E26 line ("LO"): "R1 2Ω" in series with "C1 82" (polarised, +); "CR1" (diode); "RV1" (varistor); "DS1" (neon lamp).

### 732A-1007 CAL PCB

Resistor ladder on the reference board: "R12 20", "R13 125", "R14 250", "R15 500", "R16 1K", "R17 2K"; posts "E18" (BRN wire), "E14 40" (RED), "E15 20" (ORN), "E16 10" (YEL), "E17 5" (GRN). On the cal PCB the wires end on a row of pins lettered "40  20  10  5 PPM" with a dashed jumper between the BRN pin and the 40 pin; "R19 35", "R20 100" (pot), "R18 500" complete the LO-side trim.

### Test points (Fig 8-5)

| TP | where it sits |
|---|---|
| TP1 | right end of R60 (SEL), on the reference-amp bias line to the CR5 / R9 / CR2 node |
| TP2 | top of R5 (asterisk) / left end of R6 (SEL) |
| TP3 | R8 (11.42K) / R11 (SEL) junction, with C17 1200 pf |
| TP4 | right end of R10 (SEL), top of the R12…R17 ladder |
| TP5 | R21 (SEL) bottom / Q3 upper leg node |
| TP6 | E9 rail, between the RT3 legs (the thermistor legs cross the rail without dots) |
| TP7 | RT3 right leg / Q3 lower leg node (which runs down to the R22 right end / CR3 junction) |
| TP8, TP9 | one short horizontal joining the RT4 right leg and the RT3 left leg (the two thermistors' mid-point); this segment is separate from the TP7 segment |
| TP10 | RT4 left leg / R22 left end / RT1 top node |
| TP11 | R51 (SEL) / R47 (8.7K) junction (R49 side) |
| TP12 | R59 (200) wiper node / R50 (SEL) top (R55 side) |
| TP13 | R56 (1K) / R53 (SEL) junction (R54 side) |
| TP14 | R52 (SEL) / R46 (8.9K) junction (R48 side) |

### Component values printed on Fig 8-5

| designator | printed value |
|---|---|
| R1 | 200 |
| R2 | 4.22K |
| R3 | 10K |
| R4 | 1.27K |
| R5 | ✱ (ref amp set) |
| R6 | SEL |
| R7 | 6.2K |
| R8 | 11.42K |
| R9 | ✱ (ref amp set) |
| R10 | SEL |
| R11 | SEL |
| R12 | 20 |
| R13 | 125 |
| R14 | 250 |
| R15 | 500 |
| R16 | 1K |
| R17 | 2K |
| R18 | 500 |
| R19 | 35 |
| R20 | 100 (pot) |
| R21 | SEL |
| R22 | 17.4K |
| R23 | 51 |
| R24 | 10 |
| R25 | 30K |
| R26 | 51 |
| R27 | 10K |
| R28 | 7.5K |
| R29 | 19.1K |
| R30 | 2.15K |
| R31 | 1K |
| R32 | 6.2M |
| R33 | 5.1M |
| R34 | 2.4M |
| R35 | 27M |
| R36 | 27M |
| R37 | 1K |
| R38 | 51K |
| R39 | 51K |
| R40 | 10K |
| R41 | 6.8M |
| R42 | 51K |
| R43 | 100K |
| R44 | 1K |
| R45 | 1K |
| R46 | 8.9K |
| R47 | 8.7K |
| R48 | 35 |
| R49 | 35 |
| R50 | SEL |
| R51 | SEL |
| R52 | SEL |
| R53 | SEL |
| R54 | 35 |
| R55 | 35 |
| R56 | 1K |
| R57 | 350 |
| R58 | 200 (pot) |
| R59 | 200 (pot) |
| R60 | SEL |
| R61 | 1M |
| R62 | 2.7, 1/2W, 5% |
| R63 | 2.7, 1/2W, 5% |
| R64 | 51 |
| RT1 | 10K 25°C |
| RT2 | 10K 25°C |
| RT3 | 10K, 25°C (oven) |
| RT4 | 10K, 25°C (oven) |
| C1 | .22 |
| C2 | .22 |
| C3 | 1 |
| C4 | 330 pf |
| C5 | .22 |
| C6 | .22 |
| C7 | 4700 pf |
| C8 | 5 |
| C9 | .47 |
| C10 | 4 |
| C11 | 270 pf |
| C12 | 100 pf |
| C13 | 100 pf |
| C14 | 180 pf |
| C15 | .22 |
| C16 | .047 |
| C17 | 1200 pf |
| CR1, CR2, CR6, CR8 | zener symbols |
| CR3, CR4, CR5, CR7 | diodes |
| Q1 | 2N3904 |
| Q2 | 2N3904 |
| Q3 | 2N3906 |
| Q4 | 2N3906 |
| Q5 | EN2484 |
| U1 | LM308A (pins 2 –, 3 +, 4, 6 out, 7, 8) |
| U2 | ✱ (ref amp set; transistor + zener in one outline) |
| U3A | LM358H (pins 2, 3, 4, 1) |
| U3B | LM358H (pins 5, 6, 7, 8) |
| U4 | LM308H (pins 2 –, 3 +, 4, 6, 7, 8) |
| U5 | LM308H (pins 2 –, 3 +, 4, 6, 7, 8) |

Term strip (off-board): R1 2Ω, C1 82, CR1, RV1, DS1.

### NOTES (verbatim)
> NOTES: UNLESS OTHERWISE SPECIFIED:
> 1. ALL RESISTANCES ARE IN OHMS.
> 2. ALL CAPACITANCES ARE IN MICROFARADS.
> 3. ✱ = REF AMP SET 732A-4502.

### REF DESIGNATIONS table (verbatim)

| HIGHEST | NOT USED |
|---|---|
| C17 | |
| CR8 | |
| E36 | E12, 13, 19, 20, 29-32 |
| Q5 | |
| R64 | |
| RT2 | |
| TP14 | |
| U5 | |

Drawing numbers "732A-1001 / -1007". Caption: "Figure 8-5. A5 Reference PCB Assembly (cont)".
