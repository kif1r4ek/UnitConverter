from pint import UnitRegistry, DimensionalityError, UndefinedUnitError

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
    """
        Convert length/area from one unit to another

        Args:
            value: Numeric value to convert
            from_unit: Source unit (e.g., "m", "cm", "m2")
            to_unit: Target unit (e.g., "km", "inch", "acre")

        Returns:
            Converted value rounded to 2 decimal places

        Raises:
            ValueError: If conversion fails

        Example:
            convert_length(1000, "m", "km")
            1.0
    """

    if from_unit not in UNITS_LENGTH_MAPPING:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in UNITS_LENGTH_MAPPING:
        raise ValueError(f"Unknown unit: {to_unit}")

    try:
        from_unit = UNITS_LENGTH_MAPPING[from_unit]
        to_unit = UNITS_LENGTH_MAPPING[to_unit]

        quantity = value * ureg.parse_expression(from_unit)
        result = quantity.to(ureg.parse_expression(to_unit))

        return round(result.magnitude, 2)
    except (DimensionalityError, UndefinedUnitError) as e:
        raise ValueError(f"Conversion error from {from_unit} to {to_unit}: {str(e)}")
    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Unexpected error during conversion: {str(e)}")
