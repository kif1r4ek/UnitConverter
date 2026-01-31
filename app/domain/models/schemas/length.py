from pydantic import Field

from app.domain.models.validator import PositiveValueValidator
from app.domain.units.length import UnitsLength


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