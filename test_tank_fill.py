"""Original-artifact, regression, invalid-input, and additional domain tests."""
import pytest
from tank_fill import calculate
from workbook_reference import read_original


def test_known_correct_original_r101():
    rows, _ = read_original()
    case = rows[0]
    assert case['run'] == 'R-101'
    assert case['formula'] == 'C6*D6*(E6/12)*7.48052'
    assert calculate(case['length_ft'], case['width_ft'], case['entered_depth_in'])['us_gallons'] == pytest.approx(299.2208)
    assert case['cached_gallons'] == pytest.approx(299.2208)


def test_original_r108_field_unit_regression():
    rows, _ = read_original()
    case = next(r for r in rows if r['run'] == 'R-108')
    assert case['field_unit'] == 'ft'
    legacy = calculate(10, 6, case['entered_depth_in'], 'in')['us_gallons']
    corrected = calculate(10, 6, case['field_depth'], case['field_unit'])['us_gallons']
    assert legacy == pytest.approx(93.5065)
    assert corrected == pytest.approx(1122.078)
    assert corrected == pytest.approx(12 * legacy)


def test_original_total_omits_last_six_runs():
    rows, total = read_original()
    assert total['formula'] == 'SUM(G6:G17)'
    legacy = sum(calculate(r['length_ft'], r['width_ft'], r['entered_depth_in'])['us_gallons'] for r in rows[:12])
    assert legacy == pytest.approx(float(total['value']))
    complete = sum(calculate(r['length_ft'], r['width_ft'], r['entered_depth_in'])['us_gallons'] for r in rows)
    assert len(rows) == 18
    assert complete == pytest.approx(13147.0139)
    corrected = sum(calculate(r['length_ft'], r['width_ft'], r['field_depth'], r['field_unit'])['us_gallons'] for r in rows)
    assert corrected == pytest.approx(14175.5854)


@pytest.mark.parametrize('args', [(0,6,8),(-10,6,8),(10,0,8),(10,6,-1),(10,6,'bad'),(10,6,None),(10,6,'nan'),(10,6,'inf'),(True,6,8),(1e308,1e308,1e308)])
def test_invalid_input_refused(args):
    with pytest.raises(ValueError): calculate(*args)


def test_unsupported_unit_refused():
    with pytest.raises(ValueError, match='unit'): calculate(10,6,8,'cm')


def test_additional_domain_case_empty_tank():
    assert calculate(10,6,0)['us_gallons'] == 0


def test_feet_and_inches_equivalent():
    assert calculate(10,6,30,'in')['us_gallons'] == calculate(10,6,2.5,'ft')['us_gallons']


def test_tank_interface_and_refusal(tmp_path):
    from app import Monitor, create_app
    client = create_app(Monitor(tmp_path)).test_client()
    assert client.get('/tank').status_code == 200
    good = client.post('/tank',data={'length_ft':'10','width_ft':'6','depth':'8','depth_unit':'in'})
    assert good.status_code == 200 and b'299.2208' in good.data
    bad = client.post('/tank',data={'length_ft':'10','width_ft':'6','depth':'-1','depth_unit':'in'})
    assert bad.status_code == 400 and b'Depth must be zero or greater' in bad.data
    empty = client.post('/tank',data={})
    assert empty.status_code == 400
