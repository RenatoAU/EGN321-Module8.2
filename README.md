# Engineering Capstone — Tank Fill and Sensor Watch
Renato Jacinto · EGN 321 · Module 8, Assignment 8.2

Repository: https://github.com/RenatoAU/EGN321-Module8.1

The silent partner observation is omitted because the student reports that the instructor made it optional. Evidence in this repository comes from automated technical verification; no partner session is claimed.

## 1. Project Overview
Sensor Watch validates classroom sensor data, stores an auditable SQLite history, replays temperature readings, and displays health and alerts in a local Flask dashboard. It replaces manual inspection of sensor CSV rows and monitoring that required the developer to watch the terminal. The capstone includes the original tank-fill calculation at `/tank` and the later sensor monitoring process at `/`. Temperature is not a depth measurement and does not feed the tank-volume formula. The two workflows share the Flask interface and application log. Intended users are classmates and lab operators reviewing simulated measurements.

## 2. System Requirements
- Python 3.10 or later, with pip. Windows examples use the `py` launcher; macOS/Linux examples use `python3`.
- Flask, waitress, and pytest as specified in `requirements.txt`. SQLite is included with Python.
- A modern browser and an available local port 5000.
- Read access to the project and CSV; write access to the runtime folder; one running supervisor per runtime folder.
- Internet for installing dependencies and obtaining the repository; normal replay runs locally without internet or physical hardware.
- No environment variables or external database server are required.
- Keep `tank_fill.py`, `workbook_reference.py`, the original workbook, `verify_workbook.py`, `app.py`, `supervisor.py`, `history.py`, `alert_logic.py`, `logging_config.py`, `templates/`, `data/`, `requirements.txt`, `pytest.ini`, and `tests/` together. The database is created automatically.

## 3. Installation
Download ZIP from https://github.com/RenatoAU/EGN321-Module8.1 using Code → Download ZIP. Extract it, open the extracted folder in VS Code, and open Terminal → New Terminal. The terminal must be in the folder containing `supervisor.py` and `requirements.txt`. If you already have the supplied folder, begin there. The instructor's repository is a reference, not the student's submission link.

Windows PowerShell:
```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe supervisor.py
```

macOS/Linux:
```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python supervisor.py
```

Open http://127.0.0.1:5000 in a browser on the same computer. Keep the terminal open. Stop with Ctrl+C. Wait for shutdown before starting again. No virtual environment activation is needed with these commands.

## 4. Quick Start
After installing once, from the project folder:
```powershell
.\.venv\Scripts\python.exe supervisor.py
```
1. Open http://127.0.0.1:5000.
2. Wait a few seconds for replay to begin; the dashboard refreshes every two seconds.
3. Check current accepted temperature, units, health, alert, and data status.
4. Select **Original Module 6 history** to inspect archived temperature readings; use **Dashboard** to return.
5. Locate `runtime/application.jsonl` and follow Section 12 to verify recovery.
6. Stop using Ctrl+C in the terminal.

On macOS/Linux use `.venv/bin/python` in place of the Windows executable. Do not start `app.py` separately when the supervisor is running.

## 5. Normal Operation
The supplied sensor CSV loads automatically on first startup; there is no upload button and no typed temperature entry. For engineering calculations, select **Tank Fill Calculator and workbook verification** or open http://127.0.0.1:5000/tank. Enter length 10 ft, width 6 ft, depth 8, unit inches, then select **Calculate volume**. Expect **299.2208 US gal**. Enter depth -1 to see a clear refusal. For R-108 enter depth 2.5 and select feet, yielding **1122.0780 US gal**. Open the original workbook under `original/` and compare the source cells listed in WORKBOOK_VERIFICATION.md. The database imports all five channels. The worker then delivers one temperature row every two seconds and saves its cursor and alert state. Read the current card only when a value is available. Inspect the raw/accepted/status columns to understand rejected input. View original timestamps on the archive page. Leave the process running to monitor replay, then stop it from the terminal.

A restart resumes the next source row in the same runtime; it does not erase history. Replay is finite: 1,756 rows take roughly 59 minutes at the default interval. When delivery finishes, health eventually becomes FAILED because no new usable reading arrives. A fresh replay requires a new runtime folder, described in Section 12.

## 6. Inputs and Units

Tank inputs: length and width are finite positive feet, depth is finite and nonnegative, and the depth selector accepts `in` or `ft`. Zero depth returns zero. Tank outputs are ft³ and US gallons using 7.48052 US gal/ft³. Missing or nonfinite numbers, negative depth, non-positive dimensions, unsupported units, or numeric overflow are refused. Tank calculations write TANK_CALCULATED or TANK_REFUSED events to the shared log.
The required source is `data/module6_sample_sensor_history.csv`: 1,756 timestamped rows, imported as 8,780 channel records. It is the Module 6 classroom dataset, not the earlier Arduino dataset. Keep the original file unchanged during the handoff.

| Field/channel | Unit | Accepted range |
|---|---|---|
| `sample_number` | positive integer | unique per channel |
| `timestamp` | ISO date/time, timezone unspecified | increasing on the 60-second source grid; missing slots allowed |
| `temperature_c` | °C | finite 0–50 inclusive |
| `humidity_percent` | % | finite 0–100 inclusive |
| `light_raw` | raw units | any finite number; no calibrated bounds enforced |
| `distance_cm` | cm | finite ≥0 |
| `potentiometer_percent` | % | finite 0–100 inclusive |

Each channel also requires its status column: `temperature_status`, `humidity_status`, `light_status`, `distance_status`, and `potentiometer_status`. A value is accepted only with source status `OK` and the range rule satisfied. Blank values or source `MISSING` become MISSING. Malformed/nonfinite values become INVALID. Other source statuses or out-of-range numbers become REJECTED. Raw text is preserved; unusable accepted values are NULL.

Optional command arguments: `--runtime folder` (default `runtime`), `--interval seconds` (default 2; use a finite positive number), `--port number` (default 5000; use an unused valid port), and `--demo` (synthetic tests only). Source sampling remains 60 seconds regardless of replay speed. No automatic unit conversion or alternative file format is provided.

## 7. What the Tool Refuses
- It does not present missing, rejected, invalid, or stale input as a current valid temperature; the card shows **Unavailable**.
- It does not substitute zero or fill missing measurements.
- Import fails for an empty CSV, missing required columns, invalid dates, non-increasing/timezone-aware timestamps, an off-grid timestamp, or duplicate archive keys.
- Startup fails for a missing/unreadable CSV or unwritable runtime database. Inspect the terminal because some initialization failures occur before a structured application error can be logged.
- A non-positive interval is rejected by the command line. Invalid port arguments or nonfinite intervals are unsupported; stop and correct them.
- A failed dashboard/database request returns HTTP 503 with FAILED. A worker error exits the child so the supervisor can restart it.

## 8. Expected Output
The main page shows current accepted temperature in °C, system health, NORMAL/ALERT, data status, latest delivery age, original source timestamp, received UTC timestamp, and up to 40 recent replay rows. `/history` shows the original temperature archive. `/api/status` returns the same monitoring state as JSON. Successful first initialization preserves 8,780 original archive records in `runtime/monitor.db`.

Source time identifies the original measurement. Received UTC identifies its accelerated replay delivery today; it is not a new physical measurement. Missing archive slots remain absent. This dashboard provides tables, not live charts. The separate `history.py` plotting workflow requires matplotlib and is outside this guide’s installation and normal workflow.

## 9. System Health and Alerts
| State | Meaning and operator response |
|---|---|
| RECOVERING | No delivery yet during startup grace period; wait for replay. |
| HEALTHY | Timely accepted input and no active threshold alert; continue observing. |
| DEGRADED | Latest unusable input, active alert, delivery older than 3 intervals, or no accepted reading for more than 3 intervals; inspect status and logs. |
| FAILED | Delivery or accepted-reading age exceeds 10 intervals; inspect source/process/database. Also returned on failed dashboard requests. |

Default stale threshold: more than 6 seconds without delivery. Default failed-age threshold: more than 20 seconds. Three consecutive accepted readings ≥30°C activate ALERT. A low or unusable reading resets the activation count; stale delivery also resets that count. Once active, only an accepted value ≤28.5°C clears the alert. Missing/rejected/stale input cannot clear it. These are classroom rules, not calibrated safety limits. No SMS/email is sent. A stopped server may make the browser unavailable instead of displaying a health state.

## 10. Logs
Default location: `runtime/application.jsonl`, rotating at 2 MB with three backups. A custom runtime changes this path accordingly. Each line is JSON with a UTC timestamp, event name, and event details. Events include startup, processed readings, health changes, alert activation/clear, stale data, errors, child interruption, restart scheduling, and recovery readiness. `RECOVERY_READY` indicates initialization completed; confirm actual recovery separately through the dashboard/API.

Windows, in a second PowerShell terminal:
```powershell
Get-Content runtime/application.jsonl -Tail 30
```
macOS/Linux:
```bash
tail -n 30 runtime/application.jsonl
```
Match event times to the interruption and resumption. A force-killed child cannot write its own final event; the supervisor records the exit. Disk or permission failure may prevent logging.

## 11. Troubleshooting
| Problem | Possible cause | Check/action |
|---|---|---|
| Python or `py` is not found | Python absent or launcher unavailable | Install/repair Python 3.10+; reopen the terminal and check the version. |
| `ModuleNotFoundError` | Wrong interpreter or missing dependencies | Repeat the exact virtual-environment pip command in Section 3. |
| Cannot find `requirements.txt`/`supervisor.py` | Terminal in wrong folder | Open the folder containing those files and retry. |
| Browser cannot connect | Server stopped, startup error, or port conflict | Inspect terminal/log; stop duplicate processes; use `--port 5001` and open port 5001. |
| Current value Unavailable | Missing, rejected, invalid, or stale input | Inspect data status, latest delivery age, and logs; do not treat the last valid value as current. |
| Replay stays FAILED after restart | Persisted cursor at end of CSV | Use a new runtime folder for a new classroom replay. |
| Database unavailable/locked | Permissions, wrong path, duplicate supervisor, disk problem | Stop duplicates; verify folder access/free space; preserve database before recovery. |
| Repeated restarts | Persistent startup/source/configuration fault | Stop supervisor with Ctrl+C, fix the first error, and restart once. |

## 12. Recovery Procedures
### Safe interruption and restart — operator handoff task
1. Record current source timestamp and system health; capture evidence before stopping.
2. Press Ctrl+C in the running supervisor terminal. Record that the dashboard stops updating or becomes unavailable.
3. Preserve `runtime/`; do not delete its database.
4. Restart with the same command from Quick Start.
5. Refresh the dashboard. Check that delivery resumes, source history is retained, and a recent accepted reading is shown (health can remain DEGRADED if an alert/input condition persists).
6. Read the log for shutdown/start events and new READING_PROCESSED events. Capture the recovery result.

The supervisor also restarts an unexpectedly exiting child after one second while the supervisor and computer remain running. The manual procedure above tests operator restart, not automatic crash recovery. It does not repair a corrupt database or a stopped supervisor.

### Ended replay or damaged runtime
Stop the supervisor. Preserve the old folder as evidence. For a separate clean replay:
```powershell
.\.venv\Scripts\python.exe supervisor.py --runtime runtime_handoff_new
```
Use a folder name that does not already exist. Logs and the new database will be under it. This reimports the supplied source and restarts its replay; it does not restore lost runtime records. If a disk/permission problem remains, correct it first. Do not overwrite or corrupt the original database for this handoff.

## 13. Assumptions
CSV values use the documented units; source timestamps have no asserted timezone. Replay runs against a reasonably accurate host clock. The dataset schema remains unchanged. Only one supervisor writes each runtime. The 0–50°C rule and warning thresholds are classroom assumptions, not physical calibration.

## 14. Known Limitations
Tank calculations assume a level rectangular tank with vertical walls. No tank height or capacity check is available, so a numerically valid result does not prove safe fill capacity. No physical sensor calibration, live serial ingestion, remote authentication, SMS/email alerts, automatic source looping, database repair, power-loss recovery guarantee, or verified boot service is provided. The web history page displays temperature only; other channels remain in SQLite. Archive gaps cannot be reconstructed. A persistent fault causes repeated restart attempts. Logs can be lost if storage fails. The built-in development evidence script is optional and does not prove that a classmate operated the app.

## 15. Testing
From the project folder:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
On macOS/Linux use `.venv/bin/python -m pytest -q`. The suite currently runs 21 cases covering workbook agreement, the R-108 unit regression, the incomplete legacy total, invalid/unsupported tank inputs, zero-depth and unit equivalence, HTTP success/refusal, alert hysteresis, archive preservation, cursor restart, stale/failed states, and missing/rejected readings. Tests create temporary databases. See `verification/TEST_RESULTS.txt` for the current automated run; it is not a partner handoff result.

Run the virtual-environment interpreter with `verify_workbook.py` to reproduce all 18 original-row comparisons. See `VERIFICATION_REPORT.md` for the automated HTTP, alert, stale-data, and process-recovery checks. See `IMPROVEMENTS.md` and `REFLECTION.md` for the documentation review. The optional silent observation was not performed.

## 16. AI Usage
See `AI_LOG.md` for a concise record of assistance and verification. Add the actual partner observations and your own local checks after performing them.

## Final delivery and presentation
Read `CAPSTONE_REPORT.md`, `WORKBOOK_VERIFICATION.md`, `VERIFICATION_REPORT.md`, and `IMPROVEMENTS.md` for the supporting evidence. `presentation/Capstone_Presentation.pptx` contains eight slides. `presentation/SPEAKER_NOTES.md` and `LIVE_DEMO.md` provide the 8–10 minute presentation sequence. Prepare with `CODE_DEFENSE.md` before class. AI may not be used during the live challenge or code defense.

The repository URL is the student-provided https://github.com/RenatoAU/EGN321-Module8.1. Upload this final package to that repository, or update GITHUB_LINK.txt if a separate 8.2 repository is created. A public URL alone does not prove that this new package has been uploaded. See SUBMISSION_CHECKLIST.md for remaining student actions.
