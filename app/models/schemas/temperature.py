from pydantic import BaseModel, field_validator
from app.domain.units.temperature import UNITS_TEMPERATURE_MAPPING


class TemperatureConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    decimals: int = 2

    @field_validator("from_unit", "to_unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        if v not in UNITS_TEMPERATURE_MAPPING:
            raise ValueError(f"Unsupported unit: {v}")
        return v
