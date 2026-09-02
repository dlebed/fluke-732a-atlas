Source: 732A Instruction Manual, PDF pages 32-37 (manual pages 4-8 through 4-13)

---

### (continued from preceding page — Line Voltage Selection procedure, PDF p32, manual p4-8)

2. Set the BATTERY OPR switch to ON and remove ac line power from the instrument.

3. Remove the AC Module.

4. Locate the voltage selector switches (slide switches, top of PCB, near rear panel). Set the switches so that the dots on the switch actuators select the correct line voltage. As shown in Figure 4-5.

5. Reinsert the AC Module, replace the screws.

6. On the rear panel, change the mark to the appropriate box, under the SUPPLY/SETTING heading, to indicate the present power configuration.

7. Replace the line fuse with one of appropriate value.

8. After verifying that the local ac line voltage matches the voltage selected on the 732A, apply ac line power to the instrument.

### 4-30. ACCEPTANCE TEST (PDF p32, manual p4-8)

4-31. Use the following procedure to verify that the instrument is operational. The required test equipment is listed in Table 4-1. Equivalent instruments may be used, provided the minimum specification is met.

1. Check the IN CAL indicator on the front panel. If illuminated, proceed to step 2. If not, complete steps a through f.

    a. If the IN CAL indicator was not lit, set the rear panel BATTERY PWR switch to OFF and apply ac power to the instrument using the Variac, to the Supply Setting limit listed on the rear panel.

    b. Adjust the Variac for 120V ac output. The ac line current should be less than 0.3A.

    c. Set the BATTERY PWR switch to ON. The ac line current should be less than 0.35A if the battery is dead (BTRY CHG indicator blinking). If BTRY CHG indicator is on steadily, the ac line current should be less than 0.35A.

    d. Allow the 732A to stabilize (under power) for 24 hours.

    e. If a standards laboratory is available, perform the External Calibration Procedure described in Section 4. If a standards laboratory is not available, send the 732A to a Fluke Technical Service Center or an independent standards laboratory for calibration.

    f. Once the 732A has been calibrated, proceed to step 2.

2. Apply ac power of the correct voltage and frequency to the instrument. The AC PWR and BTRY CHG indicators should both be on.

3. Measure the value of the Oven Temperature Thermistor at the front panel binding posts with Multimeter A. The value should be within ±1 ohm of the value shipped with the instrument.

4. Check the output voltage at the 10V output using Multimeter A. It should be accurate within the performance limitations of the Multimeter.

5. Measure the change in output voltage under load. To make this measurement correctly, wire Multimeter A to the 10V and 10V LO binding posts (do not use plugs) and measure the voltage. Then plug the 1000 ohm load into the same binding posts and measure the voltage. The voltage change should be less than 50 uV or 5.0 ppm.

6. Repeat step 4 for the 1V and 1.018V outputs.

7. If a standards laboratory is available, verify stability by comparison to standard cells or another pre-certified 732A. This step is optional.

8. The instrument is operational.

### 4-32. CALIBRATION (PDF p32, manual p4-8)

4-33. Complete either of the following calibration procedures to certify the 732A. Procedure A uses direct comparison between the Unit Under Test (UUT) and a Certified 732A to calibrate the 10V output. The 10V output of the UUT is then transferred to a stable adjustable voltage source. The voltage source is then divided down, as required, for comparison with the UUT 1.018V and 1V outputs. Procedure B transfers the voltage from a bank of standard cells to a stable adjustable voltage source, then divides the voltage source down, as required, for comparison with the UUT.

4-34. Either procedure may be used, taking into account the available test equipment and the degree of accuracy needed. The necessary equipment for each procedure is listed in Table 4-1.

### 4-35. Null Verification (PDF p32, manual p4-8)

4-36. Use the following procedure to verify the accuracy of null in the calibration procedures. The Null Verification procedure identifies the thermal voltages present and allows the null adjustment to be made independently of them. Use the Null Verification procedure in the two calibration procedures (Procedures A and B) when instructed to "verify the null".

1. Adjust the UUT for zero on the Null Detector.

2. Reverse the HI and LO (positive and negative) leads on the UUT and RU (Reference Unit).

3. Observe the Null Detector reading. If the reading does not equal zero, adjust the UUT for one-half of the Null Detector reading.

4. Reverse the HI and LO (positive and negative) leads on the UUT and Certified 732A. The Null Detector should have the same reading as it did at the end of step 3. If not, adjust the UUT for one-half the difference.

5. Repeat steps 2 through 4 until the Null reading does not change when the UUT and Certified 732A leads are reversed.

6. The residual reading on the Null Detector equals the sum of the thermal voltages in the circuit.

### 4-37. Procedure A:Calibrate to Certified 732A (PDF p33, manual p4-9)

4-38. Complete the following procedure to standardize the outputs of the 732A to a Certified 732A. Battery operation of the 732A and 845AB/AR is preferred. Set the Null Detector to ZERO when changing leads. Use the supplied adjustment tool for all adjustments (Fluke P/N 686113).

1. Perform the self-calibration procedure on the Precision Divider immediately prior to this procedure.

2. Obtain a certified 732A.

3. Connect the UUT and the Certified 732A as shown in Figure 4-6.

4. Set OPR switch on the Null Detector to the ZERO position, then switch power on. Adjust the Null Detector for zero on the 3 µV range.

5. Set the Null Detector to the 30µV range and the OPR switch to OPR.

6. Decrease the range setting on the Null Detector slowly while adjusting the 10V calibration potentiometer, through the front panel opening on the UUT, for a null indication on the Null Detector on the 3µV range. Let the system stabilize for about 1 minute before adjustment. Use the non-conducting adjustment tool supplied with instrument.

7. Verify the null.

8. Connect the equipment as shown in Figure 4-7. Set the Precision Divider ratio switches to 0.999999X.

9. Adjust the Adjustable Source for a null indication.

10. Verify the null.

11. Connect the equipment as shown in Figure 4-8. Set the Precision Divider ratio switches to 0.1018000.

12. Set the Null Detector RANGE switch to the 3 volt range, then connect the Input lead to the UUT 1.018V terminal. Switch the Null Detector to OPR.

13. Adjust the 1.018V calibration potentiometer on the UUT while decreasing the RANGE setting on the Null Detector to obtain a null on the 3 µV range. Use the non-conducting adjustment tool.

14. Verify the null.

15. Set the Presicion Divider ratio switches to 0.1000000.

16. Transfer the Null Detector input lead from the 1.018V terminal to the 1V terminal on the UUT.

17. Set the RANGE control on the Null Detector to the 3 volt position. Adjust the 1V calibration potentiometer on the UUT while decreasing the RANGE setting on the Null Detector to obtain a null indication on the 3 µV range. Use the non-conducting adjustment tool.

18. Verify the null.

19. If the IN CAL indicator is illuminated, proceed to step 20. If not, connect a short wire to one of the front panel COMMON terminals. Momentarily touch the other end of this wire to the circuit board behind the RESET hole. The IN CAL indicator should illuminate.

20. Calibration is complete. Record all test results. Disconnect all test equipment. Cover the output adjustment access holes and the RESET hole with tamper-proof calibration seals.

#### Figure 4-6. 732A Procedure 'A' 10V Calibration (PDF p33, manual p4-9)

Three instrument panels, connected by wires as shown:

- **CERTIFIED 732A** (left panel): binding posts labeled, top row **10V**, **LO**; middle row **1.018V**, **LO**, **1V**; bottom row **GND**, **GRD**.
- **NULL DETECTOR** (middle panel): binding posts **HI**, **LO**, **GRD** (top to bottom).
- **UUT** (right panel): binding posts, top row **10V**, **LO**; middle row **1.018V**, **LO**, **1V**; bottom row **GND**, **GRD**.

Connections: CERTIFIED 732A 10V post is wired (its 10V and LO leads pass together through a twisted-pair loop, shown as a small oval/loop symbol beside the panel) to the Null Detector HI post. The UUT 10V post is wired (its 10V and LO leads likewise pass through a twisted-pair loop) to the Null Detector LO post. The CERTIFIED 732A LO post is wired along the bottom of the figure to the UUT LO post. The CERTIFIED 732A GND post is wired to the Null Detector GRD post, and a tail from the Certified-side twisted-pair loop joins this ground wire; the UUT GRD post is wired only to a tail from the UUT-side twisted-pair loop. The Null Detector HI/LO leads also pass through a twisted-pair loop symbol. CERTIFIED 732A GRD and UUT GND posts have no wires.

---

### 4-39. Procedure B: Calibration to Standard Cells (PDF p34-35, manual p4-10/4-11)

4-40. Use the following procedure to standardize the output of the 732A. Set the Null Detector to ZERO when changing leads or when not making measurements to avoid accidental damage to the Standard Cells. Observe the techniques presented in Section 2 for minimizing thermal emf errors.

**CAUTION**

To prevent damage to the standard cells, the null detector used must open circuit its input leads when the ZERO/OPR Switch is set to the ZERO position.

1. Perform the self-calibration procedure on the Precision Divider immediately prior to this procedure.

2. Measure the standard cell enclosure temperature per the manufacturer's instructions and compute the voltage of up to 9 standard cells connected in series. Call this voltage S.

3. Set the Null Detector to the ZERO position.

4. Connect the equipment as shown in Figure 4-9A.

5. Adjust the ZERO control on the Null Detector for a zero indication on the 3 µV range.

6. Set the RANGE switch to the 300uV range.

7. Set the Precision Divider ratio switches to S/10.

8. Adjust the Adjustable Source for precisely 10V output.

9. Set the Null Detector to OPR. If the Null Detector reading exceeds ± 300 µV, quickly return the Null Detector to the ZERO position and determine the reason for the imbalance.

**NOTE**

*If a high degree of imbalance exists, check the output of the Precision Divider at its output terminals using Multimeter A. It should be approximately equal to the total voltage of the Standard Cell bank, or S.*

10. Adjust the Adjustable Source for a null indication on the Null Detector. This is a preliminary null.

11. Set the Null Detector to the ZERO position on the 3 uV range. Adjust the ZERO control if necessary for a zero indication.

12. Disconnect the lead going from the positive terminal of the Standard Cells to the Null Detector at the Standard Cell end as shown in Figure 4-9B. Connect this lead to the negative terminal of the Standard Cells at the standard cell enclosure as shown in Figure 4-9C.

13. Set the Precision Divider ratio switches to 0.000000.

14. Set the Null Detector to the OPR postion and wait for a stable reading. Note any offset (residual reading). This reading represents the extraneous and thermal voltages which should be less than 0.5 µV. If the offset exceeds this value, the cause should be investigated and corrected before proceeding. Adjust the Null Detector ZERO control to obtain a null indication.

15. Return the Null Detector to the ZERO position. Do not disturb the setting of the ZERO control.

16. Set the Precision Divider ratio switches to the previously calculated value of S/10.

17. Reconnect the positive lead of the Standard Cells as shown in Figure 4-9A.

18. Readjust the Adjustable Source, if necessary, for a null indication on the 3 µV range of the Null Detector.

19. Do not change the setting on the Adjustable Source or the leads to the Precision Divider.

20. Connect the equipment as shown in Figure 4-10.

21. Repeat steps 12 through 15 for the UUT. In Step 12, move the lead from the 10V HI terminal to the 10V LO terminal of the UUT.

22. Set the Precision Divider ratio switches to 0.999999X.

23. Set the Null Detector to the 300 µV range and set the OPR/ZERO switch to the OPR position.

24. Decrease the range setting on the Null Detector slowly while adjusting the 10V calibration potentiometer, through the front panel opening on the UUT, for a null indication on the Null Detector. Use the non-conducting adjustment tool supplied with the instrument.

25. Adjust the 10V calibration potentiometer to obtain a null indication with the Null Detector on the 3 µV range. Let the system stabilize for about 1 minute before adjustment.

26. Connect the equipment as shown in Figure 4-11. Reset the Null Detector to the 3V range.

27. Set the Precision Divider to 0.1018000.

28. Decrease the range setting on the Null Detector slowly while adjusting the 1.018V calibration potentiometer, through the front panel opening on the UUT, for a null indiction on the Null Detector. Use the non-conducting adjustment tool supplied with the instrument.

29. Adjust the 1.018V calibration potentiometer to obtain a null indication with the Null Detector on the 3 µV range. Let the system stabilize for about 1 minute before adjustment. Verify the null.

30. Move the wire connected to the UUT 1.018V output to the UUT 1V output. Reset the Null detector to the 3V range.

31. Set the Precision Divider to 0.1000000.

32. Decrease the range setting on the Null Detector slowly while adjusting the 1V calibration potentiometer, through the front panel opening on the UUT, for a null indication in the Null Detector. Use the non-conducting adjustment tool.

33. Adjust the 1.V calibration potentiometer to obtain a null indication with the Null Detecor in the 3 uV range. Let the system stabilize for about 1 minute before adjustment. Verify the null.

34. If the IN CAL indicator is illuminated, go to step 35. If not, connect a short wire to one of the front panel COMMON terminals. Momentarily touch the other end of this wire to the circuit board [continues on next page — not included in PDF pages 32-37]

#### Figure 4-9. 732A 10V Calibration Using Standard Cells (PDF p36, manual p4-12)

Three sub-figures (A, B, C), each showing four instrument panels: **ADJUSTABLE SOURCE**, **PRECISION DIVIDER**, **NULL DETECTOR**, **STANDARD CELLS**.

- **ADJUSTABLE SOURCE** panel (all three sub-figures): binding posts **HI**, **SENSE +**, **SENSE −**, **LO**, **GRD**, **GND**. HI and SENSE+ are both wired (their leads pass through a tall loop) to the Precision Divider **1.0** terminal (the **1.1** terminal is drawn with no wire connected to it); SENSE− and LO are both wired (through a second tall loop) to the Precision Divider **LO** terminal. GRD and GND are jumpered together; GND is wired to the Null Detector **GRD** terminal, to the bottom of the first tall loop (the bottom of the second tall loop is wired to the Precision Divider input **GND**), and to the twisted-pair loop on the Precision Divider output leads.
- **PRECISION DIVIDER** panel: input terminals **1.1**, **1.0**, **LO**, **GND**, inside the labeled box. Ratio annotation at top right: **0.999999X** (sub-figure A), **S10** (sub-figures B and C — i.e., the S/10 ratio setting). A second terminal cluster — **HI**, **LO**, **GND** — is drawn inside the box at its right side; its HI is wired (through a twisted-pair loop symbol) to the Null Detector **HI** terminal, its LO is wired along the bottom of the figure to the Standard Cells **−** terminal, and its GND has no wire.
- **NULL DETECTOR** panel: terminals **HI**, **LO**, **GRD**; the HI and LO leads pass through a twisted-pair loop symbol.
- **STANDARD CELLS** panel: terminals **+** and **−**.

**A.** Standard Cells + terminal wired to Null Detector LO; Standard Cells − terminal wired to the Precision Divider output LO (both Standard Cell leads pass through a twisted-pair loop symbol). (Normal/measurement connection — positive lead connected.)

**B.** Same as A but the lead from Null Detector LO is lifted off the Standard Cells + terminal and a hand icon is shown holding its free end beside the **−** terminal, illustrating disconnecting the lead from the Standard Cells positive terminal at the standard-cell end (per step 12). The − terminal remains wired to the Precision Divider output LO.

**C.** Standard Cells + terminal left unconnected; the lead formerly from + (from Null Detector LO) is now shown connected to the Standard Cells **−** terminal, which also retains its lead to the Precision Divider output LO (per step 12/13, lead moved to the negative terminal).

#### Figure 4-10. 732A Procedure 'B' 10V Calibration (PDF p37, manual p4-13)

Four panels: **ADJUSTABLE SOURCE**, **PRECISION DIVIDER**, **NULL DETECTOR**, **732A UUT**.

- **ADJUSTABLE SOURCE**: terminals **HI**, **SENSE +**, **SENSE −**, **LO**, **GRD**, **GND**, wired the same way as Figure 4-9 (HI and SENSE+ both to Precision Divider 1.0, with 1.1 left unconnected; SENSE− and LO both to Precision Divider LO; GRD/GND jumpered, with GND wired to Null Detector GRD, to the first tall loop, and to the twisted-pair loop on the Precision Divider output leads; second tall loop to Precision Divider input GND).
- **PRECISION DIVIDER**: input terminals **1.1**, **1.0**, **LO**, **GND**; ratio shown as **0.999999X**. A second terminal cluster (**HI**, **LO**, **GND**) inside the box at its right side has its HI wired (through a twisted-pair loop symbol) to Null Detector **HI**, its LO wired along the bottom of the figure to the UUT top-row **LO** post, and its GND left unwired.
- **NULL DETECTOR**: terminals **HI**, **LO**, **GRD** (the HI and LO leads pass through a twisted-pair loop symbol).
- **732A UUT**: binding posts, top row **10V**, **LO**; middle row **1.018V**, **LO**, **1V**; bottom row **GND**, **GRD**. UUT 10V wired (through a twisted-pair loop symbol) to Null Detector LO; UUT top-row LO wired to the Precision Divider output LO; UUT GRD wired to the twisted-pair loop on the UUT leads; UUT GND has no wire.

#### Figure 4-11. Calibration of 1.081V (and 1V) to 732A Procedure 'B' (PDF p37, manual p4-13)

Same four-panel layout as Figure 4-10 (**ADJUSTABLE SOURCE**, **PRECISION DIVIDER**, **NULL DETECTOR**, **732A UUT**), with the same HI/SENSE+ → Precision Divider **1.0** wiring (1.1 unconnected) and the same **HI**/**LO**/**GND** output cluster inside the right side of the Precision Divider box, its HI feeding Null Detector **HI** (through a twisted-pair loop symbol), and Precision Divider ratio shown as **0.1018000 (0.1000000)** — the parenthetical value used for the 1V calibration. The Null Detector LO lead is shown connected to the UUT **1.018V** terminal, and the UUT middle-row **LO** terminal is wired to the Precision Divider output LO; the UUT **10V**/**LO** top-row posts have no wires in this figure. UUT GRD is wired to the twisted-pair loop on the UUT leads; Adjustable Source GND is wired to Null Detector GRD, to the twisted-pair loop on the Precision Divider output leads and to the small twisted-pair loop on the Null Detector input leads.

**NOTE: MOVE 1.018V ON UUT TO 1V FOR 1V CALIBRATION.**

---

Note: Figure 4-8 (PDF p34) is identical in structure to Figure 4-7/4-11 pattern — see "Figure 4-8. Calibration of 1.081V (and 1V) to 732A Procedure 'A'" transcribed below since it falls within Procedure A (step 11-17), on PDF p34.

#### Figure 4-7. Calibration of Point A to 10V Using 732A (PDF p34, manual p4-9/4-10 area)

Four panels: **ADJUSTABLE SOURCE**, **PRECISION DIVIDER**, **NULL DETECTOR**, **732A RU**.

- **ADJUSTABLE SOURCE**: terminals **HI**, **SENSE +**, **SENSE −**, **LO**, **GRD**, **GND**. HI and SENSE+ both wired (leads through a tall loop) to Precision Divider **1.0** (the **1.1** terminal is drawn with no wire connected to it); SENSE− and LO both wired (through a second tall loop) to Precision Divider **LO**; GRD/GND jumpered, with GND wired to Null Detector **GRD**, to the bottom of the first tall loop (the second tall loop's bottom is wired to Precision Divider input **GND**), and to the twisted-pair loop on the Precision Divider output leads.
- **PRECISION DIVIDER**: input terminals **1.1**, **1.0** (circled "A" annotation below/beside the 1.0 terminal marking "Point A"), **LO**, **GND**, inside the labeled box; ratio shown as **0.999999X**. A second terminal cluster — **HI**, **LO**, **GND** — is drawn inside the box at its right side; its HI is wired (through a twisted-pair loop symbol) to Null Detector **HI**, its LO is wired along the bottom of the figure to the 732A RU top-row **LO** post, and its GND has no wire.
- **NULL DETECTOR**: terminals **HI**, **LO**, **GRD** (the HI and LO leads pass through a twisted-pair loop symbol).
- **732A RU**: binding posts, top row **10V**, **LO**; middle row **1.018V**, **LO**, **1V**; bottom row **GND**, **GRD**. RU 10V wired (through a twisted-pair loop symbol) to Null Detector LO; RU top-row LO wired to the Precision Divider output LO; RU GRD wired to the twisted-pair loop on the RU leads; RU GND has no wire.

#### Figure 4-8. Calibration of 1.081V (and 1V) to 732A Procedure 'A' (PDF p34, manual p4-10)

Four panels: **ADJUSTABLE SOURCE**, **PRECISION DIVIDER**, **NULL DETECTOR**, **732A UUT**.

- **ADJUSTABLE SOURCE**: terminals **HI**, **SENSE +**, **SENSE −**, **LO**, **GRD**, **GND**, wired as in Figure 4-7 (HI/SENSE+ to Precision Divider 1.0, 1.1 left unconnected; GND to Null Detector GRD and to the twisted-pair loop on the Precision Divider output leads).
- **PRECISION DIVIDER**: input terminals **1.1**, **1.0**, **LO**, **GND**; ratio shown as **0.1018000 (0.1000000)**. A second terminal cluster (**HI**, **LO**, **GND**) inside the box at its right side has its HI wired (through a twisted-pair loop symbol) to Null Detector **HI**, its LO wired along the bottom of the figure to the UUT middle-row **LO** terminal, and its GND left unwired.
- **NULL DETECTOR**: terminals **HI**, **LO**, **GRD** (the HI and LO leads pass through a twisted-pair loop symbol).
- **732A UUT**: binding posts, top row **10V**, **LO**; middle row **1.018V**, **LO**, **1V**; bottom row **GND**, **GRD**. Null Detector LO wired (through a twisted-pair loop symbol) to the UUT **1.018V** terminal; UUT middle-row **LO** wired to the Precision Divider output LO; UUT GRD wired to the twisted-pair loop (junction dot) on the UUT leads; UUT 10V, top-row LO and GND have no wires.

**NOTE: MOVE 1.018V ON UUT TO 1V FOR 1V CALIBRATION.**

[transcriber note: no jumpers or A7 Calibration PCB references (jumper names / ppm values) appear anywhere in the text or figures on PDF pages 32-37; this section covers §4-29(partial)/4-30 through 4-40 and does not reach the A7 board adjustment procedure, which appears to be described later in Section 4]
