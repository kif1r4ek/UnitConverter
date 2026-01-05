from pint import UnitRegistry

ureg = UnitRegistry()

UNITS_WEIGHT_MAPPING = {
    "mg": "milligram",
    "g": "gram",
    "kg": "kilogram",
    "ton": "tonne",
    "oz": "ounce",
    "lb": "pound",
    "stone": "stone",
    "ton_us": "short_ton",
}

def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    try:
        from_unit = UNITS_WEIGHT_MAPPING[from_unit]
        to_unit = UNITS_WEIGHT_MAPPING[to_unit]

        quantity = value * ureg.parse_expression(from_unit)
        result = quantity.to(ureg.parse_expression(to_unit))

    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Conversion error: {str(e)}")

    return round(result.magnitude, 2)
