from pydantic import BaseModel, Field, field_validator


class ConversionRequest(BaseModel):
    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Current unit")
    to_unit: str = Field(..., description="Target unit")

    @field_validator('value')
    def value_must_be_positive(cls, v, from_unit):
        if v < 0:
            raise ValueError('Value must be positive')
        return v

    @field_validator("from_unit", "to_unit")
    def units_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Unit cannot be empty')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "value": 100,
                "from_unit": "m",
                "to_unit": "km"
            }
        }

class ConversionResponse(BaseModel):
    result: float = Field(..., description="Converted value")
    original_value: float = Field(..., description="Original value")
    from_unit: str = Field(..., description="Current unit")
    to_unit: str = Field(..., description="Target unit")

    class Config:
        json_schema_extra = {
            "example": {
                "result": 0.1,
                "original_value": 100,
                "from_unit": "m",
                "to_unit": "km"
            }
        }