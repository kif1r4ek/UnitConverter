from pint import DimensionalityError, UndefinedUnitError

from app.dependencies.common import ureg
from app.domain.exceptions import (
    UnsupportedUnitError,
    DimensionalityConversionError,
    ConversionError
)
from app.domain.units.length import UNITS_LENGTH_MAPPING, UnitsLength


def convert_length(value: float, from_unit: UnitsLength, to_unit: UnitsLength, decimals: int = 2) -> float:
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
    try:
        from_unit = UNITS_LENGTH_MAPPING[from_unit]
        to_unit = UNITS_LENGTH_MAPPING[to_unit]

        quantity = value * ureg.parse_expression(from_unit)
        result = quantity.to(ureg.parse_expression(to_unit))

        return round(result.magnitude, decimals)
    except KeyError as e:
        raise UnsupportedUnitError(str(e))
    except DimensionalityError as e:
        raise DimensionalityConversionError(from_unit, to_unit)
    except UndefinedUnitError as e:
        raise UnsupportedUnitError(str(e))
    except Exception as e:
        # Позже здесь будет logger
        raise  ConversionError(f"Unexpected error during length conversion: {str(e)}")
