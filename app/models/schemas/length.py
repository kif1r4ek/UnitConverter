from pydantic import field_validator
from app.domain.units.length import UNITS_LENGTH_MAPPING
from app.models.forms import ConversionRequest



class SLengthConvertRequest(ConversionRequest):
    value: float
    from_unit: str
    to_unit: str
    decimals: int = 2

    @field_validator("from_unit", "to_unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        if v not in UNITS_LENGTH_MAPPING:
            raise ValueError(f"Unsupported unit: {v}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "value": 100,
                "from_unit": "m",
                "to_unit": "km"
            }
        }