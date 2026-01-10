from pydantic import field_validator
from app.models.forms import ConversionRequest


class PositiveValueValidator(ConversionRequest):

    @field_validator('value')
    @classmethod
    def value_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Value must be positive')
        return v