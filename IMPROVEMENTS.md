# Problems Discovered and Improvements

These changes result from documentation and source review. They were not observations of a classmate.

| Problem before | Change made | Result after / validation |
|---|---|---|
| Setup assumed the right terminal folder and used global pip, which can install dependencies into the wrong interpreter. | Added the project-folder requirement, virtual environment creation, and exact interpreter paths for Windows and macOS/Linux in README Section 3. | Installation, testing, and startup now consistently use one environment. The application entry point and requirements match the source; Windows execution was not tested here. |
| Startup, optional evidence generation, and boot configuration were mixed together, making the normal workflow harder to locate. | Added a separate Quick Start and normal operation sequence, explaining that the supplied CSV loads automatically and no upload button is required. | Operators now have a single documented path from startup to dashboard/history. Automated HTTP checks verify the dashboard and archive routes. |
| Recovery instructions did not clearly distinguish a child crash, stopping the supervisor, and exhausting the finite replay. | Added a safe manual restart procedure, fresh-runtime instructions, exact log commands, and explicit distinction between manual and automatic recovery. | Technical evidence verifies automatic child restart, retained archive records, and database integrity. The guide explains why an exhausted cursor requires a separate runtime. |

The silent partner observation was optional according to the student's instructor clarification and was omitted. No changes are described as resulting from an unperformed partner test.

## Final-delivery calculation improvement
The saved monitor did not expose the inherited tank calculation. The final application adds /tank with explicit depth units, reusable finite/range validation, calculation/refusal logging, and a workbook comparison. The R-108 discrepancy is shown with both source interpretations. HTTP and calculation tests verify the new workflow.
