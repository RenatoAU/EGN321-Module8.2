"""Reproduce comparisons directly from the unchanged supplied workbook."""
import csv
import hashlib
import json
from pathlib import Path
from tank_fill import calculate
from workbook_reference import read_original, ORIGINAL


def main():
    root = Path(__file__).resolve().parent
    rows, total = read_original()
    results = []
    for row in rows:
        same = calculate(row['length_ft'], row['width_ft'], row['entered_depth_in'], 'in')['us_gallons']
        field = calculate(row['length_ft'], row['width_ft'], row['field_depth'], row['field_unit'])['us_gallons']
        assert abs(same - row['cached_gallons']) < 1e-7
        results.append(dict(**row, app_as_entered_gallons=same, app_field_units_gallons=field))
    summary = dict(artifact_sha256=hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
                   original_total_formula=total['formula'], original_cached_total=float(total['value']),
                   total_all_rows_as_entered=sum(r['app_as_entered_gallons'] for r in results),
                   total_all_rows_field_units=sum(r['app_field_units_gallons'] for r in results),
                   source_runs=len(rows), all_cached_row_values_match=True)
    output = root/'evidence'
    output.mkdir(exist_ok=True)
    (output/'workbook_verification.json').write_text(json.dumps(dict(summary=summary, cases=results), indent=2))
    with (root/'data/tank_reference_cases.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader(); writer.writerows(results)
    lines = ['# Original Workbook Verification', '',
             'Source: original/TANK_FILL_rev4.xlsx, preserved unchanged. Formula text and cached values are read directly from the XLSX. This script does not recalculate Excel.', '',
             '| Run | Workbook cell | Cached US gal | App using entered inches | App using field-note units |',
             '|---|---|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['run']} | Tank Fill!{r['cell']} | {r['cached_gallons']:.4f} | {r['app_as_entered_gallons']:.4f} | {r['app_field_units_gallons']:.4f} |")
    lines += ['', '## Findings', '',
              '- Known-correct R-101: 10 ft × 6 ft × (8 in / 12) × 7.48052 = 299.2208 US gal, matching Tank Fill!G6.',
              '- R-108: Tank Fill!E13 contains 2.5 under an inches header, while Field Notes!E11 says 2.5 ft. Legacy G13 = 93.5065 US gal. Using the field-note unit gives 1122.0780 US gal. The app requires an explicit unit selection and does not silently resolve contradictory sources.',
              f"- Original total G25 uses {total['formula']} and caches {summary['original_cached_total']:.4f} US gal. This includes 12 of the 18 runs.",
              f"- All 18 rows using the entered inches sum to {summary['total_all_rows_as_entered']:.4f} US gal.",
              f"- All 18 rows using field-note units sum to {summary['total_all_rows_field_units']:.4f} US gal. This is the result under the explicitly stated decision to use Field Notes for R-108.",
              '- The repeated conversion literals /12 and 7.48052 are replaced by named constants in tank_fill.py.',
              '- Invalid input: negative depth produces a ValueError and HTTP 400 refusal. Additional application-specific test: zero depth gives zero volume. Both are automated tests.',
              '', '## Reproduction', '', 'Run `python verify_workbook.py` from the project root (use the virtual-environment interpreter in the README). The CSV and JSON record each source cell, formula, cached result, and application comparison.', '',
              'Artifact SHA-256: '+summary['artifact_sha256'], '',
              'The comparison proves the rectangular-volume calculation for these cases. It does not establish actual tank dimensions, capacity, field measurement accuracy, or sensor calibration.']
    (root/'WORKBOOK_VERIFICATION.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__': main()
