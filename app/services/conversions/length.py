from pint import UnitRegistry, DimensionalityError, UndefinedUnitError
from app.dependencies.common import ureg
from app.domain.units.length import UNITS_LENGTH_MAPPING


def convert_length(value: float, from_unit: str, to_unit: str, decimals: int = 2) -> float:
    """
        Convert length/area from one unit to another

        Args:
            :param value: Numeric value to convert
            :param from_unit: Source unit (e.g., "m", "cm", "m2")
            :param to_unit: Target unit (e.g., "km", "inch", "acre")
            :param decimals: Number of decimal places to round to

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

        return round(result.magnitude, decimals)
    except (DimensionalityError, UndefinedUnitError) as e:
        raise ValueError(f"Conversion error from {from_unit} to {to_unit}: {str(e)}")
    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Unexpected error during conversion: {str(e)}")
