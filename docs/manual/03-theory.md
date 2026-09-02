Source: PDF pages 21-24 (manual pages 3-1 through 3-4)

# Section 3
# Theory of Operation

### 3-1. INTRODUCTION (PDF p21, manual p3-1)

3-2. The information in this section describes the theory of operation of the 732A. It contains an overall functional description followed by a circuit description of the 732A. Both descriptions are supported by a block diagram (Figure 3-1). Component level descriptions contained in the circuit analysis are referenced to the detailed schematics in Section 8 of this manual.

### 3-3. OVERALL FUNCTIONAL DESCRIPTION (PDF p21, manual p3-1)

3-4. The 732A dc Voltage Referance Standard is a highly stable 10V, 12 mA power supply. Refer to Figure 3-1. AC line input power is full wave rectified and fed to a two stage voltage regulator. The first stage, or Pre-regulator converts the raw dc to 32V dc. The second stage, or Regulator converts this voltage to 18.5V dc which powers the Oven Controller and the Reference.

3-5. The Voltage Monitor disables the Oven Controller and latches the IN CAL indicator off when the output of the Regulator is insufficient for proper operation. The RESET terminal is used to restore the IN CAL indicator to the ON condition after standardization of the instrument has been performed.

3-6. If ac line power fails or is not available, an internal, sealed, lead-acid battery maintains operating power to the 732A. When ac power is available, a battery charger charges the battery. This is indicated by the BTRY CHG indicator.

3-7. When ac power is not available, the battery may be charged by an external ac or dc source connected at the rear panel POWER INPUT connectors. The external source can also supply operating power for the instrument. The battery voltage can also be measured at the rear panel connectors.

### 3-8. CIRCUIT DESCRIPTION (PDF p21, manual p3-1)

3-9. The information in this section describes the circuitry of the 732A to the functional block diagram level. Refer to the detailed schematics in Section 8.

### 3-10. Power Supplies (A3 and A4) (PDF p21, manual p3-1)

3-11. The 732A has two cascaded regulators. The Pre-regulator (A3Q1) is a simple emitter follower regulator that clamps the full wave rectified power from the bridge rectifier to approximately 32V dc.

3-12. The Regulator (located on A4) supplies operating voltages to all of the circuitry in the 732A except the battery charger. During battery operation, the battery drives the Regulator input.

3-13. The Regulator (Q1, Q2, Q3, Q4) is a conventional series pass transistor error-amplifier design that regulates the 32V to 18.6V dc.

### 3-14. Voltage Monitor (PDF p21, manual p3-1)

3-15. The Voltage Monitor circuit (Q5, Q6, Q7, Q8) checks the regulator output and disables the instrument when the supply voltage falls below a critical value. When this happens, the Oven Controller is disabled and the IN CAL indicator is latched off. The reset circuit is used to turn the IN CAL indicator back on after standardization has been re-verified by qualified personnel. The Voltage Monitor is located on the A4 Regulator PCB.

3-16. Transistor Q8 is turned on by the voltage drop across the Regulator circuit series-pass transistor. This causes switching transistor Q5 to saturate, supplying power to the Oven Controller circuit and the IN CAL indicator circuit. When the output falls below that needed for normal operation, Q8 and Q5 turn off, shutting down the Oven Controller and removing drive from Q7, a Programmable Unijuction Transistor (PUT). This removes the drive from Q6, shutting off the IN CAL indicator on the front panel. When power is restored, Q7 remains latched off until its emitter is connected monemtarily to the COMMON output terminal via the RESET connection, accessible through the front panel.

### 3-17. Reference Circuit, A5 (PDF p22, manual p3-2)

3-18. The Reference Circuit (A4Q12, Q1, Q2, Q5, U1, U2) reduces the 18.6V output of the Regulator to precisely 10V. The Reference circuit is a highly stable series-pass voltage regulator. The entire reference supply (except the pass transistor) is enclosed in an oven to provide the consistent thermal environment necessary for the stability of the output.

3-19. U2, the Ref-Amp, is a transistor and zener diode mounted on a common substrate. This construction compensates for ambient temperature changes, thus U2 has an extremely low temperature coefficient. The Ref-Amp compares the 10V output to its internal zener reference to derive an error voltage which is amplified by op amp U1. U1 drives the series pass element (Q1, A4Q12). Q2 provides current limiting to protect the series pass element under short circuit conditions. Variable resistor R20 allows a small adjustment (±50 uV) in the output voltage of the Reference. Larger adjustments can be made by jumper changes on the Calibration PCB Assembly, A7.

### 3-20. Output Divider (PDF p22, manual p3-2)

3-21. Two precision resistive voltage dividers divide the precise 10V output down to 1V and 1.018V. Each of these dividers is adjustable over a limited range to allow calibration. Both dividers are enclosed in the oven with the reference.

### 3-22. Oven Controller (PDF p22, manual p3-2)

3-23. The Oven Controller (A4Q13, A4Q14, Q3, Q4, U3, U4, U5) maintains the internal temperature of the oven at a nominal temperature of 48 ± 2°C. The Oven Controller is a high thermal gain, proportional control circuit. The Oven Controller circuit is partially located on the A5 Reference PCB assembly, inside of the oven. The oven driver and output transistors are located on the A4 Regulator PCB assembly.

3-24. Thermistors RT1, series connected RT2, and RT3 are connected in a bridge configuration with R28 and R29, and are located inside the oven. U3 buffers the bridge output and drives differential amplifier/integrator U5 which drives the oven driver and output transistors (A4Q13, A4Q14) and subsequently the oven heaters. U4 shapes the overall loop frequency response.

### 3-25. Battery Charger (PDF p22, manual p3-2)

3-26. The battery charger determines the state of the charge of the internal battery and sets the charging current accordingly: constant current charging for deep discharge or constant voltage trickle charging for charge maintenance. The Battery Charger circuit is located on A3.

3-27. Transistor Q2 is a current source that supplies all the charging current. Transistors Q3 and Q4 form a schmitt trigger. Transistor Q6 supplies a constant voltage output for trickle charging and thus maintains the battery at full charge. Three thermistors monitor the ambient temperature (RT1) and the battery temperature (A6RT1, A6RT2) and adjust the charging rate accordingly.

3-28. During initial charging, Q3 enables Q2 and the high charge rate. When the battery voltage rises to approximately 32V, Q4 turns off, shutting off the constant current charge. The battery is then constant voltage charged by Q6 (approximately 27V at 23°C). Potentiometer R10 sets the threshold point of this transition and hence the end of charge current. At this point, Q6 supplies a constant voltage trickle charge to the battery and R20 sets this voltage level. Thermistor A3RT1 compensates the constant voltage charging for variations in the ambient temperature. Thermistors RT1 and RT2, located on the battery PCB, and Q5 prevent high current charging at temperatures below 5°C, and/or high temperatures.

### Figure 3-1. Functional Block Diagram (PDF p23, manual p3-3/3-4)

Overall geometry: a large dashed-line box labeled "OVEN" encloses two blocks — "A5 REFERENCE, Q1,Q2,Q5,U1,U2,A4,Q12" (left, with an "OUTPUT DIVIDER" sub-block above it and, separately, a free-standing thermistor symbol wired only to "OVEN TEMP THERMISTOR TERMINALS" above it) and "OVEN CONTROLLER, Q3,Q4,U3,U4,U5" (right). A plain oval "HEATER" block sits on the line that runs from the junction dot on the "18.5V dc" line (just before A5 REFERENCE) to the OVEN CONTROLLER; beside it, a separate thermistor symbol (circle with a zig-zag resistor glyph inside) is wired to the OVEN CONTROLLER by a single lead — the HEATER oval itself carries no symbol. Below the oven box are "A4 REGULATOR, Q1,Q2,Q3,Q4" and "VOLTAGE MONITOR, Q5,Q6,Q7,Q8". Below that are "A3 PRE-REGULATOR, Q1" and "BATTERY CHARGER, Q2,Q3,Q4,Q5,Q6", plus "A6 BATTERY" and a "BATTERY OPR" switch. At the bottom are the AC line input transformer (two primary windings, two inter-winding shield lines, one secondary winding with a two-diode rectifier stack) feeding a common unregulated dc bus that is separate from the "32V dc" node above it, and the rear-panel POWER INPUT, which enters through a diode at the BATTERY CHARGER/A6 BATTERY junction rather than at that bus. Indicator LEDs (AC PWR, BTRY CHG, IN CAL) and front-panel terminals (RESET, GUARD, and the oven-related output terminals) are shown at their respective blocks.

Blocks and labels (verbatim):
- "A5 REFERENCE / Q1,Q2,Q5,U1,U2,A4,Q12" (inside OVEN dashed box)
- "OUTPUT DIVIDER" (sub-block above A5 REFERENCE, inside OVEN box)
- "OVEN CONTROLLER / Q3,Q4,U3,U4,U5" (inside OVEN dashed box)
- "HEATER" (plain oval block, no internal symbol, on the line from the "18.5V dc" junction dot to the OVEN CONTROLLER, inside OVEN box)
- "A4 REGULATOR / Q1,Q2,Q3,Q4"
- "VOLTAGE MONITOR / Q5,Q6,Q7,Q8"
- "A3 PRE-REGULATOR / Q1"
- "BATTERY CHARGER / Q2,Q3,Q4,Q5,Q6"
- "A6 BATTERY"
- "BATTERY OPR" (switch, between A3/Battery Charger block group and A6 BATTERY)
- Terminals (top of diagram): "10V TERMINAL", "1.018V TERMINAL", "1V TERMINAL", "OVEN TEMP THERMISTOR TERMINALS", "IN CAL (LED)", "RESET TERMINAL", "GUARD TERMINAL"
- Indicator LEDs: "AC PWR (LED)" (at A3 PRE-REGULATOR), "BTRY CHG (LED)" (at BATTERY CHARGER)
- Voltage labels: "18.5V dc" (A4 REGULATOR output to A5 REFERENCE / OVEN block), "32V dc" (A3 PRE-REGULATOR output to A4 REGULATOR, and via a diode to the BATTERY OPR switch)
- "enable/disable" (label on the line from VOLTAGE MONITOR up to OVEN CONTROLLER only)
- AC input labels (bottom): "100-132V AC", "200-264V AC", "SAFETY GROUND", "CHASSIS GND"
- Rear panel input: "POWER INPUT / 24-40V DC / OR / 24-30V AC"

Signal/connection list (from -> to (label)) — traced from the drawn wires and junction dots; a crossing with no dot is not a connection:
- 100-132V AC and 200-264V AC primary windings (magnetically coupled only; no wire drawn from them) -> transformer secondary winding -> two-diode rectifier stack between junction dots (with a tap from the secondary to the middle dot) -> common unregulated dc bus (bottom of diagram)
- Between the primary and secondary windings are two vertical shield lines: one carries a junction dot to SAFETY GROUND and ends at the CHASSIS GND symbol; the other runs down and along the bottom edge to GUARD TERMINAL. Neither is connected to the unregulated dc bus.
- POWER INPUT (24-40V DC or 24-30V AC, rear panel) -> diode (conducts toward the junction) -> junction dot on the line between BATTERY CHARGER (output) and A6 BATTERY (not the unregulated dc bus and not the "32V dc" node)
- common unregulated dc bus -> A3 PRE-REGULATOR (raw input, two lines)
- common unregulated dc bus -> BATTERY CHARGER (raw input, two lines)
- A3 PRE-REGULATOR -> AC PWR (LED)
- A3 PRE-REGULATOR (output) -> "32V dc" node -> A4 REGULATOR (input)
- "32V dc" node -> diode (points left/toward the 32V dc node, i.e. blocks current flowing from the 32V dc node into the switch) -> BATTERY OPR switch (top contact)
- BATTERY CHARGER -> BTRY CHG (LED)
- BATTERY CHARGER (output) -> junction dot (POWER INPUT diode joins here) -> second junction dot (BATTERY OPR switch's bottom contact) -> A6 BATTERY
- BATTERY OPR switch, when closed, ties that BATTERY CHARGER/A6 BATTERY junction to the diode leading to the "32V dc" node — this is the path by which A6 BATTERY -> (through the switch and diode) -> "32V dc" node drives the Regulator input when ac fails
- A4 REGULATOR -> "18.5V dc" -> junction dot (inside the OVEN dashed boundary) -> A5 REFERENCE (powers Reference; the same line crosses the OVEN dashed boundary)
- A4 REGULATOR (output pin) -> VOLTAGE MONITOR (input, sensed regulator output)
- VOLTAGE MONITOR (one output, labeled "enable/disable") -> straight up -> OVEN CONTROLLER (bottom pin)
- VOLTAGE MONITOR (second output) -> up -> IN CAL (LED) (this line crosses the OVEN-box-to-GUARD line without a dot, i.e. without connecting to it)
- VOLTAGE MONITOR (third output) -> up -> RESET TERMINAL (this line likewise crosses the OVEN-box-to-GUARD line without a dot)
- OVEN dashed box (junction dot on its boundary) -> junction dot on GUARD TERMINAL's line (the oven enclosure and GUARD share this node; IN CAL and RESET lines cross it with no dots)
- GUARD TERMINAL's line continues down the right edge of the diagram, along the bottom edge, and up to the second transformer inter-winding shield line (see above)
- A5 REFERENCE (top) -> junction dot -> "10V TERMINAL" (up) and -> OUTPUT DIVIDER (right), i.e. OUTPUT DIVIDER taps the same node as the 10V TERMINAL, not in series before it
- OUTPUT DIVIDER -> "1.018V TERMINAL"
- OUTPUT DIVIDER -> "1V TERMINAL"
- free-standing thermistor symbol (circle) -> "OVEN TEMP THERMISTOR TERMINALS" — its two leads run only up to these terminals; no line is drawn connecting it to the OVEN CONTROLLER block
- "18.5V dc" junction dot -> HEATER (oval) -> OVEN CONTROLLER — single wired path, all inside the OVEN dashed box (no wire from A5 REFERENCE to the HEATER)
- thermistor symbol (circle, beside the HEATER) -> OVEN CONTROLLER — one lead from the resistor glyph to the block; the symbol's two through-leads end free
