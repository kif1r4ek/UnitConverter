from pint import DimensionalityError, UndefinedUnitError

from app.dependencies.common import ureg
from app.domain.exceptions import (
    UnsupportedUnitError,
    DimensionalityConversionError,
    ConversionError
)
from app.domain.units.weight import UNITS_WEIGHT_MAPPING, UnitsWeight


def convert_weight(value: float, from_unit: UnitsWeight, to_unit: UnitsWeight, decimals: int = 2) -> float:
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
    try:
        from_unit = UNITS_WEIGHT_MAPPING[from_unit]
        to_unit = UNITS_WEIGHT_MAPPING[to_unit]

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
        raise ConversionError(f"Unexpected error during weight conversion: {str(e)}")
