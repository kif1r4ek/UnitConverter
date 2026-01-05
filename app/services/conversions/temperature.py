from pint import UnitRegistry, DimensionalityError, UndefinedUnitError

ureg = UnitRegistry()

UNITS_TEMPERATURE_MAPPING = {
    "celsius": "degC",
    "fahrenheit": "degF",
    "kelvin": "kelvin"
}

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
        Convert temperature from one unit to another

        Args:
            value: Numeric value to convert
            from_unit: Source unit ("degC", "degF", "kelvin")
            to_unit: Target unit ("kelvin", "degC", "degF")

        Returns:
            Converted value rounded to 2 decimal places

        Raises:
            ValueError: If conversion fails

        Example:
            convert_temperature(0, "celsius", "fahrenheit")
            32.0
    """

    if from_unit not in UNITS_TEMPERATURE_MAPPING:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in UNITS_TEMPERATURE_MAPPING:
        raise ValueError(f"Unknown unit: {to_unit}")

    try:
        from_unit = UNITS_TEMPERATURE_MAPPING[from_unit]
        to_unit = UNITS_TEMPERATURE_MAPPING[to_unit]

        quantity = ureg.Quantity(value, from_unit)
        result = quantity.to(to_unit)

        return round(result.magnitude, 2)
    except (DimensionalityError, UndefinedUnitError) as e:
        raise ValueError(f"Conversion error from {from_unit} to {to_unit}: {str(e)}")
    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Unexpected error during conversion: {str(e)}")







