from pydantic import BaseModel, Field, field_validator


class ConversionRequest(BaseModel):
    """
    Request model for unit conversion.

    Validates incoming conversion requests from users.
    Ensures the value is positive and units are not empty.

    Example:
        request = ConversionRequest(value=100, from_unit="m", to_unit="km")
        request.value
        100.0

    Attributes:
        :param value: numeric value to be converted
        :param from_unit: source unit of measurement
        :param to_unit: target unit of measurement
        :param decimals: Number of decimal places to round to
    """

    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Current unit")
    to_unit: str = Field(..., description="Target unit")
    decimals: int = 2

    @field_validator('value')
    @classmethod
    def value_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Value must be positive')
        return v

    @field_validator("from_unit", "to_unit")
    @classmethod
    def units_must_not_be_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError('Unit cannot be empty')
        return v



class ConversionResponse(BaseModel):
    """
    Response model containing the conversion result.

    Attributes:
        :param result: converted value
        :param original_value: original input value
        :param from_unit: source unit of measurement
        :param to_unit: target unit of measurement
    """

    result: float = Field(..., description="Converted value")
    original_value: float = Field(..., description="Original value")
    from_unit: str = Field(..., description="Current unit")
    to_unit: str = Field(..., description="Target unit")
