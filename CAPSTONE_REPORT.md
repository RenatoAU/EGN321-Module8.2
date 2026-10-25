# Capstone Delivery
Renato Jacinto · EGN 321 · Assignment 8.2

## What I inherited
The original artifact is `original/TANK_FILL_rev4.xlsx`, preserved unchanged. It records 18 tank fills. The Tank Fill worksheet accepts length and width in feet and depth under an inches header, then calculates US gallons with `length × width × (depth/12) × 7.48052`. Field Notes preserves the technician's written measurements. The rectangular-tank formula assumes level fill and vertical walls. The workbook does not independently establish actual tank height or measurement accuracy.

Inspection identified three concrete weaknesses: repeated unlabeled conversion literals, R-108's mismatch between 2.5 feet in Field Notes!E11 and 2.5 under the inches header in Tank Fill!E13, and a total in G25 that sums only G6:G17 despite data through G23. R-108 therefore produces 93.5065 US gal from the entered inches while its field-note unit yields 1122.0780 US gal. The original total is 8527.7928 US gal. All 18 entered rows total 13147.0139 US gal. Using the stated field-note unit for R-108 gives 14175.5854 US gal. The report presents both interpretations rather than silently resolving the source discrepancy.

## What the final application does
The final Flask application has two workflows. `/tank` runs the reusable rectangular-volume calculation with explicit depth units, input refusal, labeled ft³/US gallon outputs, and calculation/refusal logging. `/` runs the later classroom temperature monitoring process with validation, SQLite history, threshold alerts, health states, logs, and supervised process recovery. `/history` displays archived temperature records, and `/api/status` supplies machine-readable monitoring status.

Temperature measurements are not converted into depth or tank volume. Combining the two workflows in the final interface preserves the original calculation and the later process-monitoring work without inventing a physical connection between them. The tank interface is a final-delivery addition to the saved Module 7 monitor, not a claim that the earlier saved ZIP already included it.

## Course capabilities and final evidence
This table maps course topics to current evidence. It does not claim to reconstruct missing historical commits or an exact module-by-module development history.

| Module topic | Current evidence |
|---|---|
| 1: defects | Original workbook and WORKBOOK_VERIFICATION.md |
| 2: units and validation | Explicit in/ft depth selection, finite/range refusals, tests |
| 3: reusable logic | tank_fill.calculate, history.validate, alert_logic.update |
| 4: interface and iteration | Flask tank form and monitoring dashboard |
| 5: simulated input | Original Module 6 classroom CSV replay with provenance labels |
| 6: historical evidence | SQLite original archive, raw/accepted/status values, history page |
| 7: unattended operation | Health and alert logic, supervisor, structured logs, recovery evidence |
| 8: operation and final delivery | Operating guide, documentation improvements, reproducible tests, presentation |

## Why trust the results within the stated limits?
The known-correct workbook case R-101 agrees at 299.2208 US gal. The unit regression test shows the twelvefold R-108 difference. Invalid negative depth is refused. The additional domain case checks that an empty tank returns zero; its purpose is to distinguish an empty tank from impossible negative depth. This additional case was prepared with AI assistance and should be reviewed and explained by the student. The complete 21-case suite also checks alert hysteresis, restart persistence, and missing/stale behavior.

Original worksheet cached values for all 18 rows match independent calculations using the entered inches. The complete total is computed over all rows, with the field-note interpretation reported separately. The workbook reader preserves formula text and cached values and does not claim Excel recalculation.

Actual HTTP evidence shows HEALTHY, ALERT, cleared alert, STALE, FAILED, MISSING, and recovered HEALTHY states under synthetic test inputs. The recovery test kills the child process, verifies a changed PID and resumed service, checks retained row counts and all 8,780 archive records, and runs SQLite integrity_check. The results and execution scope are in VERIFICATION_REPORT.md and evidence/verification.json.

## Handoff and improvement
The silent partner observation was omitted because the student reports that the instructor made it optional. No partner struggle is invented. Assignment 8.1 improvements include exact virtual-environment commands, a distinct normal workflow, clarified timestamps, explicit log paths, and recovery guidance. The final tank form additionally exposes the depth unit beside its input and returns a specific refusal reason. See IMPROVEMENTS.md.

## Assumptions and limitations
Tank geometry is rectangular with a level fill and vertical walls. The application uses the workbook convention 7.48052 US gal/ft³, not a physical calibration. Length/width are feet, and depth is in or ft. Tank height is unavailable, so overfill cannot be checked. Sensor source timestamps have unspecified timezone, while replay receipt uses UTC. Source sampling is 60 seconds and replay delivers every two seconds by default. The archive has missing slots that are preserved.

The system has no live depth sensor, calibration verification, remote authentication, production deployment hardening, or automatic database repair. Restart depends on a surviving supervisor and working storage. Finite replay eventually ends and becomes stale. Browser screenshots and Windows execution are not established by the automated Linux evidence.
