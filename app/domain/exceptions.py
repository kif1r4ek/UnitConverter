"""
Custom exceptions for unit conversion application.

This module defines domain-specific exceptions that are raised
when conversion operations fail due to invalid input or unsupported units.
"""


class ConversionError(Exception):
    """
    Base exception for all conversion-related errors.

    Use this as a parent class for specific conversion errors,
    or raise it directly when you need a generic conversion error.

    Example:
        raise ConversionError("Cannot convert negative temperature to Kelvin")
    """
    pass


class UnsupportedUnitError(ConversionError):
    """
    Raised when trying to use a unit that is not supported.

    Example:
        raise UnsupportedUnitError("parsec")
    """

    def __init__(self, unit: str):
        self.unit = unit
        super().__init__(f"Unsupported unit: '{unit}'")


class InvalidValueError(ConversionError):
    """
    Raised when the input value is invalid for conversion.

    Examples:
        raise InvalidValueError("Value cannot be negative for weight")
        raise InvalidValueError("Value must be a number")
    """
    pass


class DimensionalityConversionError(ConversionError):
    """
    Raised when trying to convert between incompatible dimensions.

    For example: meters to degrees, kilograms to liters.

    Example:
        raise DimensionalityConversionError("m", "degC")
    """

    def __init__(self, from_unit: str, to_unit: str):
        self.from_unit = from_unit
        self.to_unit = to_unit
        super().__init__(
            f"Cannot convert between incompatible units: '{from_unit}' to '{to_unit}'"
        )


class NegativeValueError(InvalidValueError):
    """
    Raised when a negative value is provided where only positive values are allowed.

    Example:
        raise NegativeValueError("weight")
    """

    def __init__(self, unit_type: str):
        self.unit_type = unit_type
        super().__init__(f"Negative values are not allowed for {unit_type}")