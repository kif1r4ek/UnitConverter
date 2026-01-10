from pydantic import Field
from app.domain.units.length import UnitsLength
from app.models.validator import PositiveValueValidator


class SLengthConvertRequest(PositiveValueValidator):
    from_unit: UnitsLength  = Field(..., description="Current unit")
    to_unit: UnitsLength  = Field(..., description="Target unit")

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "value": 100,
                "from_unit": "m",
                "to_unit": "km"
            }
        }