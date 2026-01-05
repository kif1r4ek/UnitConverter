from pint import UnitRegistry

ureg = UnitRegistry()

UNITS_LENGTH_MAPPING = {
    "mm": "millimeter",
    "cm": "centimeter",
    "m": "meter",
    "km": "kilometer",
    "inch": "inch",
    "foot": "foot",
    "yard": "yard",
    "mile": "mile",
    "m2": "meter**2",
    "km2": "kilometer**2",
    "hectare": "hectare",
    "acre": "acre",
    "sqft": "square_foot"
}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    try:
        from_unit = UNITS_LENGTH_MAPPING[from_unit]
        to_unit = UNITS_LENGTH_MAPPING[to_unit]

        quantity = value * ureg.parse_expression(from_unit)
        result = quantity.to(ureg.parse_expression(to_unit))

    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Conversion error: {str(e)}")

    return round(result.magnitude, 2)
