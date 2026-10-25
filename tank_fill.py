"""Rectangular tank calculation with explicit units and refusal rules."""
import math

INCHES_PER_FOOT = 12.0
US_GALLONS_PER_CUBIC_FOOT = 7.48052  # Preserve the inherited workbook convention.


def number(value, label):
    if isinstance(value, bool):
        raise ValueError(f'{label} must be a finite number.')
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f'{label} must be a finite number.') from None
    if not math.isfinite(result):
        raise ValueError(f'{label} must be a finite number.')
    return result


def calculate(length_ft, width_ft, depth, depth_unit='in'):
    """Return ft³ and US gallons. Zero depth is an empty tank, not an error."""
    length = number(length_ft, 'Length')
    width = number(width_ft, 'Width')
    depth = number(depth, 'Depth')
    if length <= 0 or width <= 0:
        raise ValueError('Length and width must be greater than zero feet.')
    if depth < 0:
        raise ValueError('Depth must be zero or greater.')
    if depth_unit not in ('in', 'ft'):
        raise ValueError('Depth unit must be in or ft. No other units are supported.')
    depth_ft = depth / INCHES_PER_FOOT if depth_unit == 'in' else depth
    cubic_ft = length * width * depth_ft
    gallons = cubic_ft * US_GALLONS_PER_CUBIC_FOOT
    if not math.isfinite(gallons):
        raise ValueError('Calculated volume exceeds the supported numeric range.')
    return dict(length_ft=length, width_ft=width, depth=depth, depth_unit=depth_unit,
                depth_ft=depth_ft, cubic_ft=cubic_ft, us_gallons=gallons)
