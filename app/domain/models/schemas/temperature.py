from pydantic import Field
from app.domain.units.temperature import UnitsTemperature
from app.domain.models.forms import ConversionRequest


class STemperatureConvertRequest(ConversionRequest):
    from_unit: UnitsTemperature  = Field(..., description="Current unit")
    to_unit: UnitsTemperature  = Field(..., description="Target unit")

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "value": 10,
                "from_unit": "celsius",
                "to_unit": "kelvin"
            }
        }