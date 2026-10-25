# Live Code Defense Preparation

Study and practice before class. AI may not be used during the live code challenge or defense.

| Instructor request | Location | What to explain and verify |
|---|---|---|
| Change temperature alert threshold | alert_logic.py, comparison `value >= 30` | Three consecutive accepted values activate it. Update the tests and dashboard threshold text consistently. |
| Change alert clear point | alert_logic.py, `value <= 28.5` | A lower clear point prevents rapid switching near the trigger. Update matching docs/UI/tests. |
| Change stale timeout | app.py, uses of `3*self.interval` | Change the health/current-value/count-reset behavior consistently. Update dashboard threshold label and tests. |
| Change accepted temperature range | app.py tick call to history.validate | Archive channel rules live separately in history.SENSORS. Explain whether the request applies to replay, archive, or both. |
| Add tank validation | tank_fill.py, calculate | Put domain validation in reusable logic, then add an accepted and refused case. |
| Change a label | templates/tank.html or templates/dashboard.html | Keep the displayed unit aligned with the actual calculation. |
| Add a log field | app.py, event calls | Pass a named JSON-compatible field and inspect the resulting log line. |
| Change conversion constant | tank_fill.py | Explain its units and why original-workbook regression expectations may change. |

## Questions to practice
1. Why divide an inch depth by 12? Because length and width use feet, so all three dimensions must use feet before multiplying.
2. Why is 2.5 ft different from 2.5 in? The same numeric depth represents twelve times as much height when interpreted in feet.
3. Why can zero depth pass while zero length fails? Zero depth describes an empty valid tank. Zero plan dimensions do not describe the supported geometry.
4. Why keep a raw value after rejection? It preserves evidence without pretending the rejected number is an accepted measurement.
5. Why do we show two timestamps? One identifies the historical source reading and the other its replay delivery.
6. Does a restarted process prove full recovery? No. Verify a changed PID, a responding HTTP route, health, record counts, and database integrity.
7. Why does restarting an exhausted replay remain stale? Its cursor is persisted. Use a separate fresh runtime to deliberately replay again.
8. Does temperature calculate tank volume? No. Tank dimensions/depth and temperature monitoring are separate workflows.

Practice: make one requested change, run the relevant test, explain its effect, then restore it or update dependent labels and documentation. Use the exact virtual-environment test command in README.md.
