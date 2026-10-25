# Speaker Notes

Recommended duration: about 8 minutes 40 seconds, including demonstrations. Practice and adjust to your actual pace.

## Slide 1

0:00–0:55. My project began with TANK_FILL_rev4.xlsx, an inherited production fill log. The workbook takes tank length and width in feet and a depth labeled in inches, then outputs US gallons. It includes 18 runs and separate field notes. Open the actual original workbook to show Tank Fill row 6, where R-101 has length 10 feet, width 6 feet, and depth 8 inches. Explain that this is a rectangular tank calculation. Converting depth to feet first gives 40 cubic feet. Multiplying by the inherited conversion convention gives 299.2208 US gallons. The original artifact is included unchanged in the submission. Source: original/TANK_FILL_rev4.xlsx, Tank Fill!C6:G6.

## Slide 2

0:55–1:50. The formula works for known-correct inputs, but input meaning and total coverage require review. Show Tank Fill E13 and Field Notes E11 for R-108. The field note says 2.5 feet while the formula treats the entered 2.5 as inches. That produces a twelvefold difference. Also show G25: its formula sums only G6:G17, excluding the last six runs. Explain that matching an existing number does not prove that its units or total range are right. The new code names its conversion constants and the interface makes the depth unit explicit. The verification report retains both interpretations of the source discrepancy. Source: WORKBOOK_VERIFICATION.md and the original workbook.

## Slide 3

1:50–2:40. The course added capabilities in stages: checking inherited assumptions, validating units, separating reusable functions, building interfaces, replaying sensor input, preserving history, and monitoring health and recovery. The final package combines the saved Module 7 monitor with a tank calculation page added for the final delivery. This table maps capabilities to final files. It does not establish an exact historical commit sequence. The sensor dataset is the later Module 6 classroom file with five channels. Temperature is not a tank-depth measurement, so the system keeps the workflows separate. Source: CAPSTONE_REPORT.md, tank_fill.py, history.py, app.py.

## Slide 4

2:40–3:25. Explain the two workflows. The tank form passes its dimensions and explicit depth unit into tank_fill.calculate, which validates values and returns cubic feet and gallons. The sensor worker validates source readings, writes archive and replay records in SQLite, updates alert state, and supplies the dashboard. Both workflows write events to the application log. supervisor.py runs the monitoring process and restarts it after an unexpected child exit. Explain that the tank calculator remains usable even though temperature monitoring has its own health state. Source: app.py, tank_fill.py, alert_logic.py, supervisor.py.

## Slide 5

3:25–5:10. Switch to the running application. Open /tank. Submit 10 feet by 6 feet with 8 inches depth and show 299.2208 US gallons. Compare the result with workbook G6. Next enter depth 2.5 and explicitly choose feet. Show 1122.0780 US gallons and explain the R-108 difference. Enter depth minus one and show the clear refusal. Refusing an impossible depth is better than returning a plausible-looking negative volume. Restore valid input. Open the sensor dashboard and history page. Explain original source time versus today's replay receipt time. The receipt timestamp indicates replay activity and does not turn historical data into a new physical measurement. Source: LIVE_DEMO.md and the live local application.

## Slide 6

5:10–6:10. Show the 21 passing test cases in the terminal and the workbook comparison report. The known-correct case anchors the new calculation to the original artifact. The R-108 regression checks the unit discrepancy. Invalid input cases include negative, missing, nonfinite, zero dimensions, unsupported units, and overflow. The additional domain test checks zero depth as a valid empty tank. This test was prepared with AI assistance and needs my own explanation. All 18 cached workbook row results agree when interpreted as entered inches. The full totals are reported separately from the incomplete legacy total. Source: tests/test_tank_fill.py, tests/test_monitor.py, evidence/workbook_verification.json.

## Slide 7

6:10–7:45. Run the separate controlled-failure script if time permits, or open its actual saved evidence. It first shows healthy input, high-temperature alert activation and clearing, then paused delivery becoming stale and failed. It also verifies missing input. It then kills the child process and verifies the new PID, responding HTTP service, resumed healthy status, retained records, and database integrity. Show those fields in evidence/verification.json and the corresponding log entries. Explain that these are synthetic classroom fault inputs at a 0.5-second delivery interval in the assistant Linux environment. The optional silent partner observation was omitted based on the instructor clarification reported by the student. Documentation improvements came from source and workflow review, so no partner struggle is claimed. Source: VERIFICATION_REPORT.md, evidence/verification.json, IMPROVEMENTS.md.

## Slide 8

7:45–8:40. Close with the limits. The tank calculation assumes a level rectangular tank with vertical walls. It does not know the tank's maximum height, so a valid calculated volume does not prove that a fill is safe. Monitoring cannot verify physical calibration, and the replay is finite. Automatic restart requires the supervisor and storage to survive. The operating guide now gives exact commands, explicit units, and evidence paths so another operator can follow it. AI helped during development and preparation, and the specific assistance is recorded in AI_LOG.md. I must understand the final code and complete the instructor's live modification and questions independently, without AI. Source: README.md, CODE_DEFENSE.md, AI_LOG.md.
