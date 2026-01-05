from pint import UnitRegistry, DimensionalityError, UndefinedUnitError

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

def convert_weight(value: float, from_unit: str, to_unit: str, decimals: int = 2) -> float:
    """
        Convert length/area from one unit to another

        Args:
            :param value: Numeric value to convert
            :param from_unit: Source unit (e.g., "mg", "ton", "lb")
            :param to_unit: Target unit (e.g., "g", "stone", "kg")
            :param decimals: Number of decimal places to round to

        Returns:
            Converted value rounded to 2 decimal places

        Raises:
            ValueError: If conversion fails

        Example:
            convert_weight(1, "kg", "lb")
            2.2
    """

    if from_unit not in UNITS_WEIGHT_MAPPING:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in UNITS_WEIGHT_MAPPING:
        raise ValueError(f"Unknown unit: {to_unit}")

    try:
        from_unit = UNITS_WEIGHT_MAPPING[from_unit]
        to_unit = UNITS_WEIGHT_MAPPING[to_unit]

        quantity = value * ureg.parse_expression(from_unit)
        result = quantity.to(ureg.parse_expression(to_unit))

        return round(result.magnitude, decimals)
    except (DimensionalityError, UndefinedUnitError) as e:
        raise ValueError(f"Conversion error from {from_unit} to {to_unit}: {str(e)}")
    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Unexpected error during conversion: {str(e)}")
