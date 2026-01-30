from pydantic import Field
from app.domain.units.weight import UnitsWeight
from app.domain.models.validator import PositiveValueValidator


class SWeightConvertRequest(PositiveValueValidator):
    from_unit: UnitsWeight  = Field(..., description="Current unit")
    to_unit: UnitsWeight  = Field(..., description="Target unit")

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "value": 1000,
                "from_unit": "g",
                "to_unit": "kg"
            }
        }