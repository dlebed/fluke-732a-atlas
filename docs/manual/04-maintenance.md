Source: 732A Instruction Manual, PDF pages 25-31 (manual pages 4-1 through 4-7)

# Section 4 Maintenance

### WARNING (PDF p25, manual p4-1)

THESE SERVICING INSTRUCTIONS ARE FOR USE BY QUALIFIED PERSONNEL ONLY. TO AVOID ELECTRICAL SHOCK, DO NOT PERFORM ANY SERVICING OTHER THAN THAT CONTAINED IN THE OPERATING INSTRUCTIONS UNLESS YOU ARE QUALIFIED TO DO SO.

### 4-1. INTRODUCTION (PDF p25, manual p4-1)

4-2. This section of the manual contains maintenance information for the 732A. This includes general maintenance procedures, an acceptance test, calibration test, calibration procedures and troubleshooting information.

4-3. The acceptance test is used as a means of verifying that the instrument is operating within specifications. Perform the acceptance test upon receipt of the instrument.

4-4. The instrument should be calibrated at an interval commensurate with the users accuracy and stability requirements. Necessary test equipment is listed in Table 4-1. Equivalent instruments may be used, provided that they meet the minimum specification(s).

NOTE

To limit thermally induced errors, use Fluke Low Thermal EMF Assembly Cable (an accessory) or copper wire, preferably shielded twisted pair, with crimped and soldered low-thermal lugs, clamped in the binding posts for all interconnections. Avoid the use of ordinary nickel-plated banana plugs.

CAUTION

To avoid cracking the plastic binding post insulator, tighten only with finger pressure. Do not use tools.

### 4-5. SERVICE INFORMATION (PDF p25, manual p4-1)

4-6. The 732A is warranted for a period of one (1) year upon delivery to the original purchaser. The WARRANTY is given on the back of the title page located in the front of this manual.

4-7. Factory authorized calibration and service for each Fluke product is available at various worldwide locations. A complete list of Fluke service centers is included with this manual. Shipping information is given in Section 2 of this manual. If requested, an estimate will be provided to the customer before any repair work is begun on instruments that are not currently under warranty.

### 4-8. GENERAL MAINTENANCE (PDF p25, manual p4-1)

### 4-9. Access Procedure (PDF p25, manual p4-1)

4-10. Use the following procedures to disassemble the 732A for adjustment or repair. Disconnect ac power connections before disassembling the 732A.

### Table 4-1. Required Test Equipment (PDF p26, manual p4-2)

| TYPE | REQUIRED SPECIFICATIONS | RECOMMENDED MODEL | PROCEDURE* |
|---|---|---|---|
| Certified 732A | As required by the user | Fluke 732A** | A, B |
| Four to Nine Cell Bank of Standard Cells | As required by the user 9152P/4 or 9 | Guildline Instruments | A, C |
| Voltage Divider | 7 decade, 0.1 ppm resolution; 0.1 ppm absolute linearity | Fluke 720A | C |
| Null Detector | 1 μV full-scale sensitivity. 10 MΩ input resistance. ZERO/OPR switch must open circuit input terminals in ZERO position. | Fluke 845AB, AR | B, C |
| Adjustable Source | 10V dc output; 1 μV resolution; 0.3 ppm + 2 μV uncertainty | Fluke 5440A | C |
| Multimeter A | 4½-digit display; 20 kΩ resistance range; 200 mV to 200V ac or dc | Fluke 8050A, 8060A | A, D, E |
| Multimeter B | 6½-digit display; 10V dc range, 100 μV resolution; 1V dc range, 10 μV resolution | Fluke 8500A, 8502A | B, E |
| Rheostat | 50 kΩ, ½W | Fluke P/N 484089 | D |
| Variac | 120V, 1A, metered | GenRad W5MT3A | D |
| Load Resistor | 1 kΩ, ½W Carbon Composition | Fluke P/N 108597 | B, D |
| Adjustment Tool | Supplied with 732A | Fluke P/N 686113 | A,B,C |

\* A = Acceptance Test
B = Calibration, procedure A.
C = Calibration, procedure B.
D = Battery charger adjustment
E = Troubleshooting

\*\*The 732A selected for use as the Certified 732A in Calibration Procedure A should be calibrated at a calibration facility whose transfer uncertainties are consistent with the user's needs.

### 4-11. COVER REMOVAL (PDF p26, manual p4-2)

4-12. Use the following procedure to access the interior of the 732A (Refer to Figure 4-1)

1. Remove all screws securing the top and/or bottom cover(s).
2. Lift the cover(s) off the instrument.

### 4-13. REAR MODULE REMOVAL (PDF p26, manual p4-2)

4-14. There are two modules located in the rear of the 732A; The AC Module and the Battery Module. Use the following procedure to remove either of the rear modules (Refer to Figure 4-2):

NOTE

Either module, but NOT both, may be removed without loss of standardization. If the AC Module is removed, ensure that the rear panel, BATTERY OPR switch is set to ON and that the battery is charged before removing the AC Module. This will insure continued standardization.

1. Remove the screws securing the module to the rear of the instrument.
2. Pull the module out from the rear of the instrument.

### Figure 4-1. Cover and Front Panel Screw Locations (PDF p27, manual p4-3)

Two-part line drawing.

Top part, labeled "TOP AND BOTTOM": a rectangular top/bottom cover panel with a screw circle at each of the four corners; two diagonal lines connect all four corner screws in an X pattern, crossing in the middle at the label "A", with an arrowhead pointing outward to each of the four corner screws.

Bottom part, labeled "LEFT AND RIGHT SIDES": a full side view of the chassis (side panel with two feet). A vertical edge at the front of the panel carries a column of five screws; arrows fan out from the label "B" to all five of these screws. Two long horizontal rows of screws run the depth of the panel (front to back), each row having one screw near the front and one screw near the back; a bowtie-shaped pair of arrows from the label "A" points left to the front screw of each row and right to the back screw of each row, marking all the screws in both rows.

Legend printed at left of the figure:
REMOVE SCREWS MARKED:
A — COVER REMOVAL
B — FRONT PANEL REMOVAL

### Figure 4-2. Rear Module Mounting Screw Locations (PDF p27, manual p4-3)

Line drawing labeled "REAR OF INSTRUMENT": two side-by-side rectangular module openings, each with four corner screws; within each rectangle diagonal arrows cross in the middle at the label "C" (so both left and right modules are each marked "C" at their centers, arrows pointing outward to the four corner screws of that module).

Caption below drawing: REMOVE SCREWS MARKED "C" TO REMOVE REAR MODULE(S).

### 4-15. REGULATOR PCB ASSEMBLY REMOVAL (PDF p27, manual p4-3)

NOTE

Since the Regulator PCB Assembly removal requires the removal of BOTH rear modules, standardization will not be maintained after this procedure.

4-16. Use the following procedure to remove the Regulator PCB Assembly from the 732A (Refer to Figure 4-3).

1. Remove the top and bottom covers.
2. With the 732A resting on its bottom, remove the screws securing the inner shield top cover and remove the shield.
3. Remove both of the rear modules.
4. Remove the screws that fasten the two T0-220 power transistors to the bottom of the chassis. Save the two insulators and the two shoulder washers. Note the positions of the insulating hardware so they can be reassembled properly.
5. Unplug the Regulator PCB Assembly from the motherboard by pulling it out towards the rear of the 732A.

### 4-17. OVEN REMOVAL (PDF p27, manual p4-3)

4-18. Use the following procedure to remove the oven assembly from the 732A (Refer to Figure 4-4)

1. Remove the top and bottom covers.
2. With the 732A resting on its bottom, remove the screws securing the inner shield cover and remove the cover.
3. Carefully pry the top foam insulating block out from the front of the instrument using a blade type screwdriver.

### Figure 4-3. Regulator PCB Assembly Removal (PDF p28, manual p4-4)

Photograph of the instrument chassis viewed from the rear/top with covers removed, showing the exposed circuit board area. Callouts:
- "REMOVE SCREWS*" with two leader lines pointing to a pair of screws on the left board (mounting the TO-220 power transistors).
- "REGULATOR PCB ASSEMBLY" with a leader line pointing to the vertical circuit board assembly at right.
- Footnote at bottom of callout column: "*CAUTION: DO NOT LOSE INSULATING WASHERS AND SHOULDER WASHERS"

### Figure 4-4. Oven Assembly Removal (PDF p29, manual p4-5)

Two photographs stacked.

Top photo: a hand using a flat blade screwdriver to pry along the edge of a rectangular foam-insulated block (the top foam insulating block) at the front of the oven assembly. Callout: "FLAT BLADE SCREWDRIVER" with leader line to the screwdriver tip.

Bottom photo: two hands grasping the mylar tabs on top of the oven assembly and pulling upward, with the wire harness visible underneath. Callout: "GRASP TABS AND PULL UPWARDS" with an outline arrow icon pointing up beside the text; a second outline up-arrow icon is printed on the photo at the tab location.

### (continued procedure, PDF p30, manual p4-6)

4. Do the same for the foam block that is now exposed.
5. Locate the two mylar tabs located on each side of the Oven Assembly.
6. Grasp both mylar tabs and pull steadily and evenly upwards.
7. Disconnect the Oven Assembly cable harness at the motherboard and at the front panel.

### 4-19. Oven Disassembly (PDF p30, manual p4-6)

4-20. Use the following procedure to disassemble the Oven Assembly. Use this procedure only if access is necessary to effect repairs on the Oven Controller circuit. Do not attempt to repair the Reference circuit.

1. Remove the Oven Assembly from the 732A.
2. Lay the instrument on its side, with its top facing you, and lay the Oven Assembly on the work surface.
3. Remove the four screws holding the inside clamshell (the inside clamshell contains the adjustment holes for the calibration potentiometers)

NOTE

Do not turn the screws on the outside clamshell as this will cause difficult disassembly and reassembly.

4. Move the wire bundle to the side and lift the heater assembly free of the Oven Assembly.
5. Lay the heater assembly to the side. The Reference PCB Assembly circuitry is now accessible.

NOTE

In most cases, repairs to the PCB assembly can be better accomplished from the component side of the PCB. If access to the bottom of the PCB is necessary, unscrew the outside four teflon standoffs.

### 4-21. Front Panel Removal (PDF p30, manual p4-6)

4-22. Use the following procedure to detach the front panel from the 732A:

1. Remove the top and bottom covers.
2. With the 732A resting on its bottom, remove the screws securing the inner shield cover and remove the cover.
3. Locate the Blue wire coming from the GUARD terminal to a solder lug riveted to the chassis. Unsolder this wire at the solder lug and pull it free.
4. Peel the decal from both of the front corner side moldings and remove the exposed screws. Refer to Figure 4-1 for screw locations.
5. Remove the front corner side moldings from the instrument.
6. The front panel is now free. Be extremely careful of the wire harness connected to the front panel binding posts. The service loop provided is quite limited.

### 4-23. Cleaning (PDF p30, manual p4-6)

CAUTION

To prevent possible damage to the front panel, do not use aromatic hydrocarbons or chlorinated solvents on the front panel of the 732A.

4-24. When the 732A is properly cared for and kept in a controlled atmosphere, cleaning is seldom required. However, any contamination, particularly oil, in the instrument can contribute to an increase in leakage which may impair accuracy.

4-25. Clean the exterior and the front panel of the 732A with a soft cloth dampened in a mild solution of detergent and water. Do not attempt to clean the interior of the instrument.

### 4-26. Fuse Replacement (PDF p30, manual p4-6)

4-27. The power fuse F1 is located on the rear panel of the 732A. If replacement is necessary, use the following rated fuses:

100V or 120V ac operation -- MDL 3/8 (3/8A slow blow)

230V or 240V ac operation -- MDL 3/16 (3/16A slow blow)

### 4-28. AC Line Voltage Change (PDF p30, manual p4-6)

4-29. The 732A may be operated from 100V, 120V, 220V, or 240V ac ± 10%. The assigned line voltage may be changed to match the available source using the following procedure. Refer to Figure 4-5.

1. Ensure that the battery is charged or an appropriate external ac or dc source is connected to the POWER INPUT jacks on the rear panel. This will maintain the unit's stanardization when ac line power is removed. The BTRY CHG indicator on the front panel will extinquish when the battery is fully charged and the 732A is stll connected to the ac power source.

### Figure 4-5. AC Line Voltage Conversion on A3 Pre-Regulator PCB Assembly (PDF p31, manual p4-7)

Line drawing of the A3 Pre-Regulator PCB Assembly (component side), with a component-position table below it.

**Board drawing.** Upper right area, bracketed together and labeled "AC LINE VOLTAGE SELECTION SWITCHES": two slide switches —
- Switch S1: printed legend "220/240" at upper left of the switch body and "100/120" at upper right; the switch body itself is drawn as two square cells, the left cell containing a small vertical oval/capsule (pill) shape and the right cell containing an open circle.
- Switch S2: printed legend "100/220" at upper left and "120/240" at upper right, switch body drawn the same way (left cell: vertical pill shape; right cell: open circle).

Below the switches, the board outline shows (left to right, top to bottom as silkscreened): C10, C9; a row containing Q2 and Q1 (both mounted on a heatsink bar); R3; CR19, TP3; CR1, CR3, CR2, TP4; C3 (large capacitor); CR15; CR11 (near Q3, drawn inside a bracket/circle); R7, R10, C4; R8, CR18, CR28, R4, DS1; C1 (large capacitor); R14; Q4, TP5, CR20; CR25, CR24, C2; CR4, CR6, R1; C5, R15, CR17, CR22, R11, W1; CR21, CR5, CR7, CR10, CR8; C6, R13, R17, Q5, CR26, TP2, R9; RT1, R6, TP1, CR12, CR9, TP6; R20, R12, CR14, CR16, Q6, R16, CR13; P3 (connector, bottom edge).

(Verified against a magnified crop of the scan: all designators above are confirmed legible. No CR23, R2, R5, or R19 designator appears on the board — an earlier pass had misread the CR3/CR2 pair near CR1 as "CR23", the diode next to Q3 as "CR7" instead of CR11, and the thermistor RT1 as "R19".)

**Switch-setting table**, four columns, one per line voltage. Each column shows two 2-position slide-switch symbols (left = switch S1, positions "100/120" top / "220/240" bottom; right = switch S2, positions "120/240" top / "100/220" bottom), with a filled dot marking the selected position:

| Line Voltage | S1 (left switch) position | S2 (right switch) position |
|---|---|---|
| 120V | 100/120 (dot at top) | 120/240 (dot at top) |
| 100V | 100/120 (dot at top) | 100/220 (dot at bottom) |
| 240V | 220/240 (dot at bottom) | 120/240 (dot at top) |
| 220V | 220/240 (dot at bottom) | 100/220 (dot at bottom) |

(Each switch symbol in the table is drawn as a two-cell rectangle with its position labels printed beside the cells — top cell "100/120", bottom cell "220/240" for the left switch of each pair; top cell "120/240", bottom cell "100/220" for the right switch of each pair — and the filled dot appears in the cell corresponding to the selected position, as tabulated above. Exception, confirmed at high zoom: in the 240V column, the left switch's top-cell label is printed "100/220" rather than "100/120" — an apparent error in the original manual's artwork, since switch S1's only two legended positions (per the board drawing above) are 100/120 and 220/240.)
