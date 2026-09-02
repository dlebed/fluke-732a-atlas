Source: Fluke 732A Instruction Manual (1983), PDF pages 38-42 (manual pages 4-14 through 4-18)

---

### (continued from calibration procedure, PDF p38, manual p4-14)

behind the RESET hole. The IN CAL indicator should illuminate.

35. Calibration is complete. Record all test results. Disconnect all test equipment. Cover the output adjustment access holes and the RESET hole with tamper-proof calibration seals.

## 4-41. SERVICE/REPAIR PROCEDURES (PDF p38, manual p4-14)

### 4-42. Introduction (PDF p38, manual p4-14)

4-43. The Battery Charger Adjustment procedure is the only field service procedure for the 732A. There is no field serviceable circuitry within the oven/reference supply assembly. All adjustments within the oven must be made at the Factory or at a Fluke Technical Service Center. The following paragraphs describe the Battery Charger adjustments for the 732A.

### 4-44. Battery Charger Adjustment Procedure (PDF p38, manual p4-14)

**CAUTION**

**This procedure will cause loss of standardization. Calibration must be performed before reuse of the instrument.**

4-45. Refer to Figure 4-8. Perform this procedure to calibrate the battery charger after repair of the battery charger circuit. The equipment required is listed in table 4-1.

1. Remove ac power from the instrument.

2. Set the BATTERY OPR switch to OFF.

3. Remove the top cover from the instrument.

4. Remove the AC Module from the instrument.

5. Locate test points TP1, TP2, and TP5 on the A3, Pre-Regulator PCB Assembly(part of the AC Module). Locate trimpots R20 and R10 and jumper wire W1, also on the AC Module.

6. Connect a 50 kΩ rheostat between TP1 and TP2. Adjust the Rheostat for maximum resistance.

7. Connect Multimeter A between TP5 and TP1. TP5 is positive with respect to TP1.

8. Reinstall the AC Module in the instrument.

9. Apply ac power to the UUT using the Variac. Adjust the Variac for the line voltage indicated on the rear of the instrument.

10. Adjust R20 for a 33.0V dc reading on Multimeter A.

11. Turn the ac power off by reducing the Variac to zero volts or by unplugging the UUT.

12. Remove jumper W1 on A2.

13. Restore ac power.

14. Connect Multimeter A between TP2 and TP1. TP2 is positive with respect to TP1.

15. Set the BATTERY OPR switch to ON.

16. Set R10 fully clockwise (CW). Multimeter A should read approximately 45 to 50V dc.

17. While observing Multimeter A, adjust the rheostat toward minimum resistance. At approximately 26V dc, the BTRY CHG indicator and CR27 (CR27 is the voltage reference for the constant current source in the battery charger circuit, located on A2) should come on. The ac line current should jump to approximately 110 mA at 115V ac (55 mA at 220V ac).

18. Adjust the Rheostat for a Multimeter A reading of 32V dc.

19. Turn R10 counter-clockwise (ccw) until the BTRY CHG indicator and CR27 go out. Note that the ac line current has dropped.

20. Adjust the Rheostat toward minimum resistance, while observing the BTRY CHG indicator. When the BTRY CHG indicator lights, CR27 lights, and the ac line current increases suddenly. Multimeter A should read between 24.5 and 26.5V dc.

21. Adjust the Rheostat until the BTRY CHG and CR27 indicators turn off. Multimeter A should indicate a dc voltage greater than +31V.

22. Disconnect all test equipment and the rheostat.

23. Remove the AC Module from the 732A.

24. Reinstall jumper W1.

25. Reinstall the AC Module.

26. Battery Charger adjustment is now complete. Perform the Calibration adjustment procedure described earlier in this section.

### Figure 4-12. Battery Charger Test Points and Adjustments on A3 Pre-Regulator PCB Assembly (PDF p39, manual p4-15)

Full-page drawing of the A3 Pre-Regulator PCB Assembly (an elongated card, notched at upper-left edge and with three mounting notches at the bottom edge, connector P3 at bottom right). All designators printed on the drawing, top to bottom, left to right:

- **S1** — 2-position slide switch, upper right (drawn with a narrow vertical bar in the left/"1" position and an open circle "O" in the right/"0" position)
- **S2** — 2-position slide switch, below S1, same style (narrow vertical bar at "1", open circle "O" at "0")
- **C10**, **C9** — two oval capacitor outlines, left side, above the heatsink bar
- Heatsink bar (two parallel horizontal rails) carrying:
  - **Q2** (left transistor on heatsink, TO-220-style outline with screw symbol, 3 leads)
  - **Q1** (right transistor on heatsink, same style, 3 leads)
- **CR19** — diode, upper right of the lower component field
- **R3** — resistor, above capacitor C3
- **C3** — large rectangular capacitor, center
- **CR1** — diode block, right of C3
- **CR3**, **CR2** — two diodes, below CR1, stacked
- **TP3** — test point, boxed/highlighted, right side
- **TP4** — test point, boxed/highlighted, below TP3
- **CR15** — diode, left side
- **R7** — resistor, below CR15
- **Q3** — transistor (drawn with a bracket/heat-tab outline), left edge
- **CR11** — diode, next to Q3
- **R10** — trimpot, boxed/highlighted, large rectangular outline, left-center
- **C4** — capacitor, below R10
- **R8** — resistor, below C4
- **R6** — resistor, below R8
- **CR18** — diode, center
- **R4** — resistor, next to CR18
- **DS1** — indicator lamp (circle), center
- **CR28** — diode, near R4/DS1
- **C1** — large rectangular capacitor, right side
- **R14** — resistor, lower left field
- **C5** — capacitor, lower left field
- **R15** — resistor, lower left field
- **Q4** — transistor, lower left field
- **CR20** — diode, center-lower
- **TP5** — test point, boxed/highlighted, center-lower
- **CR25** — diode, right-center
- **CR24** — diode, right field
- **C2** — oval capacitor, right field
- **R1** — resistor (vertical), far right edge
- **C6** — capacitor, far left
- **R13** — resistor, left field
- **CR17** — diode, left field
- **CR22** — diode, center-left (below Q4, above R16)
- **CR21** — diode, center-left
- **R11** — resistor, center
- **W1** — jumper wire, boxed/highlighted (underlined designator), center
- **Q5** — transistor, center-left lower
- **Q6** — transistor, below Q5 and left of CR26
- **CR26** — diode, center
- **TP2** — test point, boxed/highlighted, center
- **CR4**, **CR6** — diodes, right field
- **R9** — resistor (vertical rectangular outline), center-right, left of the CR4/CR6/CR5/CR7 diode grid
- **CR5**, **CR7** — diodes, right field, below CR4/CR6
- **TP1** — test point, boxed/highlighted, far lower-left
- **RT1** — thermistor, lower-left, next to TP1
- **R18** — resistor, lower-left
- **R17** — resistor, lower-left
- **CR16** — diode, lower-center
- **CR13** — diode, lower-center
- **CR10**, **CR8** — diodes, lower-right field
- **CR12**, **CR9** — diodes, lower-right field
- **TP6** — test point, boxed/highlighted, lower right
- **R20** — trimpot, boxed/highlighted, large rectangular outline, lower-left
- **R12** — resistor, lower-center
- **CR14** — diode, lower-center
- **P3** — connector designator, bottom right corner, above the card-edge mounting notches

Boxed/highlighted (outlined in a rectangle to call out as the adjustment/test points used in the procedure): **TP1, TP2, TP3, TP4, TP5, TP6, R10, R20, W1**.

Caption: "Figure 4-12. Battery Charger Test Points and Adjustments on A3 Pre-Regulator PCB Assembly"

---

## 4-46. TROUBLESHOOTING (PDF p40, manual p4-16)

### 4-47. Introduction (PDF p40, manual p4-16)

4-48. The information in this section describes troubleshooting procedures for the 732A. The section is divided into two parts: External Symptom Troubleshooting and Internal Voltage Measurements.

### 4-49. External Symptom Troubleshooting (PDF p40, manual p4-16)

4-50. Use Table 4-2 to isolate problems within the 732A, using external symptoms. Table 4-1 lists the required test equipment for trouleshooting.

### 4-51. Internal Voltage Measurements (PDF p40, manual p4-16)

**WARNING**

**TO AVOID ELECTRICAL SHOCK HAZARD, OBSERVE THE FOLLOWING PRECAUTIONS WHILE WORKING ON THE INSIDE OF THE 732A. REMOVE ANY JEWELRY BEFORE BEGINNING TESTING. HIGH VOLTAGE AC MAY BE PRESENT DURING THE FOLLOWING TESTS, DO NOT PERFORM ALONE. EXERCISE APPROPRIATE CAUTION TO AVOID ELECTRICAL SHOCK WHEN WORKING IN OR AROUND THE VICINITY OF THE AC POWER CONNECTOR, FUSEHOLDER, AND POWER TRANSFORMER. THE BATTERY ASSEMBLY IS CAPABLE OF GENERATING EXTREMELY HIGH PEAK CURRENTS. AVOID ACCIDENTAL SHORTING OF BATTERY TERMINALS.**

**CAUTION**

**The following tests are conducted with power applied to the instrument. To avoid instrument damage, exercise appropriate caution to avoid inadvertently shorting adjacent test points or circuit board traces with test probes or other instrument(s).**

**CAUTION**

**To insure continued instrument performance, do not attempt to replace individual wires in the reference output wiring harness. Replace the entire harness.**

4-52. Use the tests shown in Table 4-3 to isolate problems to the major functional circuit groups of the 732A. It is assumed that the external symptoms given in Table 4-2 have been examined and that the primary circuit of the power transformer is operable. This procedure is conducted with the instrument energized, observe the previously stated WARNINGS and CAUTIONS.

### 4-53. Oven Repair (PDF p40, manual p4-16)

4-54. Shifts in the output level which cannot be compensated for by adding or removing jumpers from the A7 Calibration PCB will require the entire Oven Assembly to be returned to Fluke and exchanged for a working unit. Do not attempt to repair the circuitry involving U1, U2, Q1, Q2, Q5, the resistors associated with TP11 through TP14, or any other component(s) associated with the aforementioned components. Special procedures and auxilliary test equipment are necessary for component replacement within the Reference circuit. Module exchange is provided as the most economical and expedient method of repair for the user.

---

### Table 4-2. External Symptom Troubleshooting (PDF p41, manual p4-17)

| SYMPTOM | PROBABLE CAUSE | ACTION |
|---|---|---|
| 732A inoperative. | Fuse blown. | Check fuse. |
| | Battery dead. | Measure battery voltage at rear panel jacks. Recharge battery. |
| | Battery opr switch set to OFF. | Visual check. |
| | 732A not plugged in. | Restore power. |
| IN CAL indicator off. | Lost ac power, battery dead. | Charge battery, verify instrument calibration. |
| Repeated fuse blowing. | AC line primary circuit. | Visual inspection. |
| | Power transformer. | (2) |
| | Bridge rectifier. | Use ohmmeter. |
| | Battery charger rectifier. | Use ohmmeter. |
| Will not run on external ac or dc source. | Ballast lamp open. | Replace lamp. |
| Output voltage drifts. | Oven or reference. | (1) |
| Temperature sensitive. | Oven. | Check oven controller circuit. |
| Output voltage not correct. | Reference. | Perform calibration procedure. |
| Output voltages not adjustable to specifications. | Reference. | (1) |
| Battery won't charge. | Defective battery. | Replace. |
| | Battery charger defective. | Troubleshoot and repair. |
| Battery won't charge from external source. | Ballast lamp open. | Replace lamp. |

(1) The Reference portion of the Oven/Reference Supply assembly is not field repairable. Refer repair to a Fluke Technical Service Center.

(2) Return instrument to Fluke Technical Service Center for service.

---

### Table 4-3: Internal Measurements* (PDF p42, manual p4-18)

| PCB | TEST POINTS | CORRECT VOLTAGE READING | CORRECTIVE ACTION |
|---|---|---|---|
| A3 | TP3, TP4 | ≤60V dc | AC line voltage, Rectifier, Power Transformer |
| A3 | TP6, TP4 | 32V dc | Pre-Regulator |
| A3 | TP2, TP1 | ≤31V dc | Battery Charger** |
| A3 | TP5, TP1 | 33.0V dc | Battery Charger** |
| A4 | TP1, TP3 | 32V dc | Pre-Regulator, Motherboard |
| A4 | TP1, TP2 | ≈18.5V dc | Regulator |
| Front Panel | 10V, COM | 10.00000V dc | Oven, Reference Supply |
| Front Panel | 1V, COM | 1.000000V dc | Output Divider*** |
| Front Panel | 1.018V, COM | 1.018000V dc | Output Divider*** |
| Rear Panel | EXT. PWR. | ≥24V dc | Battery |

*Voltage measurements taken with Multimeter A, except for those marked with *** in corrective action column.

**Conditions: battery installed, BATTERY OPR switch ON.

***Calibration of 10V output affects calibration of this output.
