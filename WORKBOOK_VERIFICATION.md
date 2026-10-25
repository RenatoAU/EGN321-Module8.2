# Original Workbook Verification

Source: original/TANK_FILL_rev4.xlsx, preserved unchanged. Formula text and cached values are read directly from the XLSX. This script does not recalculate Excel.

| Run | Workbook cell | Cached US gal | App using entered inches | App using field-note units |
|---|---|---:|---:|---:|
| R-101 | Tank Fill!G6 | 299.2208 | 299.2208 | 299.2208 |
| R-102 | Tank Fill!G7 | 392.7273 | 392.7273 | 392.7273 |
| R-103 | Tank Fill!G8 | 448.8312 | 448.8312 | 448.8312 |
| R-104 | Tank Fill!G9 | 561.0390 | 561.0390 | 561.0390 |
| R-105 | Tank Fill!G10 | 673.2468 | 673.2468 | 673.2468 |
| R-106 | Tank Fill!G11 | 804.1559 | 804.1559 | 804.1559 |
| R-107 | Tank Fill!G12 | 897.6624 | 897.6624 | 897.6624 |
| R-108 | Tank Fill!G13 | 93.5065 | 93.5065 | 1122.0780 |
| R-109 | Tank Fill!G14 | 972.4676 | 972.4676 | 972.4676 |
| R-110 | Tank Fill!G15 | 1065.9741 | 1065.9741 | 1065.9741 |
| R-111 | Tank Fill!G16 | 1122.0780 | 1122.0780 | 1122.0780 |
| R-112 | Tank Fill!G17 | 1196.8832 | 1196.8832 | 1196.8832 |
| R-113 | Tank Fill!G18 | 523.6364 | 523.6364 | 523.6364 |
| R-114 | Tank Fill!G19 | 617.1429 | 617.1429 | 617.1429 |
| R-115 | Tank Fill!G20 | 710.6494 | 710.6494 | 710.6494 |
| R-116 | Tank Fill!G21 | 822.8572 | 822.8572 | 822.8572 |
| R-117 | Tank Fill!G22 | 935.0650 | 935.0650 | 935.0650 |
| R-118 | Tank Fill!G23 | 1009.8702 | 1009.8702 | 1009.8702 |

## Findings

- Known-correct R-101: 10 ft × 6 ft × (8 in / 12) × 7.48052 = 299.2208 US gal, matching Tank Fill!G6.
- R-108: Tank Fill!E13 contains 2.5 under an inches header, while Field Notes!E11 says 2.5 ft. Legacy G13 = 93.5065 US gal. Using the field-note unit gives 1122.0780 US gal. The app requires an explicit unit selection and does not silently resolve contradictory sources.
- Original total G25 uses SUM(G6:G17) and caches 8527.7928 US gal. This includes 12 of the 18 runs.
- All 18 rows using the entered inches sum to 13147.0139 US gal.
- All 18 rows using field-note units sum to 14175.5854 US gal. This is the result under the explicitly stated decision to use Field Notes for R-108.
- The repeated conversion literals /12 and 7.48052 are replaced by named constants in tank_fill.py.
- Invalid input: negative depth produces a ValueError and HTTP 400 refusal. Additional application-specific test: zero depth gives zero volume. Both are automated tests.

## Reproduction

Run `python verify_workbook.py` from the project root (use the virtual-environment interpreter in the README). The CSV and JSON record each source cell, formula, cached result, and application comparison.

Artifact SHA-256: 939fb835dd83d98f9ca58d7cd5430c67661636b7bf8b8c1a4690cbfed32b1f41

The comparison proves the rectangular-volume calculation for these cases. It does not establish actual tank dimensions, capacity, field measurement accuracy, or sensor calibration.
