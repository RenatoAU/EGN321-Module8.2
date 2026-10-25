# Technical Verification Report

Actual automated execution in the assistant Linux environment on October 25, 2026. Fault inputs were synthetic and delivered at 0.5-second intervals. This is not a partner session, Windows run, or physical sensor verification.

## Calculation and interface
- `python3 -m pytest -q`: **21 passed in 1.31 seconds**.
- `python3 verify_workbook.py`: all 18 cached workbook row results agree when using the original entered inches.
- Known-correct R-101: 299.2208 US gal.
- R-108 field-note interpretation: 1122.0780 US gal, versus 93.5065 US gal from the legacy inch interpretation.
- Original G25 sum: 8527.7928 US gal. All rows as entered: 13147.0139 US gal. All rows using field units: 14175.5854 US gal.
- Flask form verification: known-correct and field-unit calculations returned HTTP 200. Negative depth returned HTTP 400 with its refusal reason.

## Failure and recovery
`python3 capture_evidence.py --no-browser` completed successfully on the final application. It ran on port 5057 with a separate test_runtime and verified actual HTTP responses.

- 24°C fixture: HEALTHY.
- Repeated 32°C fixture: ALERT activated.
- Accepted 27°C fixture: alert cleared.
- Paused delivery: STALE/DEGRADED followed by FAILED.
- Empty/source-MISSING fixture: MISSING with no accepted current value.
- Killed child PID: 7. Restarted PID: 13.
- Replay records before: 7. After recovery: 8.
- Original archive records preserved: 8780.
- SQLite integrity_check: ok.
- Recovered HTTP state: HEALTHY.

## Evidence index
| Location | Contents |
|---|---|
| evidence/workbook_verification.json | Original formulas, cached values, independent results, totals, artifact hash |
| WORKBOOK_VERIFICATION.md | Human-readable comparison and interpretation |
| data/tank_reference_cases.csv | Each source case with cells and computed results |
| evidence/tank_known_correct.html | Actual form response for R-101 |
| evidence/tank_field_units.html | Actual form response using 2.5 ft |
| evidence/tank_refused.html | Actual negative-depth HTTP refusal response |
| evidence/01_dashboard_healthy.* | Healthy HTTP state and HTML |
| evidence/02_original_history.html | Archive HTML response |
| evidence/03_alert_active.* and 04_alert_cleared.* | Alert behavior |
| evidence/05_stale.*, 06_failed.*, 07_missing.* | Refusal/health conditions |
| evidence/08_recovered_healthy.* | Response following restart |
| evidence/verification.json | Complete machine-readable recovery observations |
| evidence/application.jsonl | Actual structured events |
| evidence/process_output.txt | Process output |
| evidence/verified_monitor.db | Tested SQLite snapshot, including archive and synthetic replay history |
| verification/TEST_RESULTS.txt | Test command, result, and scope |

HTML files are saved responses, not screenshots. The database snapshot is technical evidence and must not be used as today's live runtime. Normal startup creates its own runtime folder. No browser screenshots are claimed. Read LIVE_DEMO.md to reproduce the evidence.
