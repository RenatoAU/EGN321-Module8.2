"""Read the unchanged legacy XLSX using Python's standard library.

This is a narrow reader for the supplied artifact, not a general Excel engine.
Formula text and stored cached results are read separately. Excel is not recalculated.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

ORIGINAL = Path(__file__).resolve().parent / 'original' / 'TANK_FILL_rev4.xlsx'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_original(path=ORIGINAL):
    with ZipFile(path) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [''.join(s.itertext()) for s in ET.fromstring(archive.read('xl/sharedStrings.xml'))]

        def sheet(name):
            cells = {}
            root = ET.fromstring(archive.read('xl/worksheets/' + name + '.xml'))
            for cell in root.findall('.//m:sheetData/m:row/m:c', NS):
                value = cell.find('m:v', NS)
                inline = cell.find('m:is', NS)
                text = value.text if value is not None else ''.join(inline.itertext()) if inline is not None else ''
                if cell.get('t') == 's':
                    text = strings[int(text)]
                formula = cell.find('m:f', NS)
                cells[cell.get('r')] = {'value': text, 'formula': formula.text if formula is not None else None}
            return cells

        tank, field = sheet('sheet1'), sheet('sheet2')
    rows = []
    for index in range(6, 24):
        field_row = index - 2
        depth, unit = field[f'E{field_row}']['value'].split()
        rows.append(dict(run=tank[f'A{index}']['value'], cell=f'G{index}',
                         length_ft=float(tank[f'C{index}']['value']), width_ft=float(tank[f'D{index}']['value']),
                         entered_depth_in=float(tank[f'E{index}']['value']),
                         field_depth=float(depth), field_unit=unit,
                         field_cell=f'E{field_row}', formula=tank[f'G{index}']['formula'],
                         cached_gallons=float(tank[f'G{index}']['value'])))
    return rows, tank['G25']
