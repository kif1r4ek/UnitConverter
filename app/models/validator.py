from pydantic import field_validator

from app.domain.exceptions import NegativeValueError
from app.models.forms import ConversionRequest


class PositiveValueValidator(ConversionRequest):
    """
        Validator for conversion requests that require positive values.

        Used for weight and length conversions where negative values don't make sense.
        Temperature can be negative, so it doesn't use this validator.
    """

    @field_validator('value')
    @classmethod
    def value_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise NegativeValueError("conversion value")
        return v