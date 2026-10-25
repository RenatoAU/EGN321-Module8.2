# Live Demonstration Guide

## Before class
Extract the project and follow README installation. In the terminal containing supervisor.py:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe verify_workbook.py
.\.venv\Scripts\python.exe supervisor.py --runtime presentation_run
```
Use a fresh runtime name if presentation_run already contains an exhausted replay. Open the workbook, browser dashboard, tank page, reports, and slides ahead of time.

## Five demonstrations
1. **Normal operation:** open http://127.0.0.1:5000/tank. Enter 10 ft, 6 ft, 8 inches. Select Calculate volume. Explain 40 ft³ and 299.2208 US gal.
2. **Workbook verification:** show original/TANK_FILL_rev4.xlsx, Tank Fill row 6. Compare G6 with the live result. Show Field Notes E11 and Tank Fill E13 for R-108. Select 2.5 feet in the app and show 1122.0780 US gal. The discrepancy requires source review.
3. **Refusal:** enter depth -1. Show Calculation refused and its reason. Explain that refusing prevents an impossible negative volume. Return to valid input.
4. **Evidence:** show the tests, WORKBOOK_VERIFICATION.md, sensor dashboard/history, and runtime log. Explain source timestamp versus replay receipt time. The normal monitor uses classroom replay, not a live physical sensor.
5. **Controlled failure and recovery:** in a second terminal run the following evidence test on a separate port/runtime:
```powershell
.\.venv\Scripts\python.exe capture_evidence.py --no-browser
```
It deliberately tests alert, stale input, failure, and automatic restart. If test_runtime already exists, stop any prior test and rename that folder before rerunning. View http://127.0.0.1:5057 while the script runs. After completion, open evidence/verification.json and evidence/application.jsonl. Show old/new PIDs, retained archive count, integrity result, and recovered HEALTHY. The script ends the test server when finished. If the live demo fails, show saved evidence and describe the observed failure accurately.

The script uses synthetic temperature inputs at 0.5-second intervals and does not modify the original CSV. Normal monitoring at port 5000 remains separate.

## Closing
Show the limitations slide. Explain that tank capacity and physical calibration are not verified. Stop the normal supervisor with Ctrl+C when finished. Complete the instructor's code challenge independently, without AI assistance.
