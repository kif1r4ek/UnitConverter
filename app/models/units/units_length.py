from enum import Enum


class UnitsLength(Enum):
    MILLIMETER: "mm"
    CENTIMETER: "cm"
    METER: "m"
    KILOMETER: "km"
    INCH: "inch"
    FOOT: "foot"
    YARD: "yard"
    MILE: "mile"

    def get_display_name(self):

        names = {
            "mm": "Millimeter (mm)",
            "cm": "Centimeter (cm)",
            "m": "Meter (m)",
            "km": "Kilometer (km)",
            "inch": "Inch (in)",
            "foot": "Foot (ft)",
            "yard": "Yard (yd)",
            "mile": "Mile (mi)",
        }

        return names[self.value]

class UnitsArea(Enum):
    SQUARE_METER: "m2"
    SQUARE_KILOMETER: "km2"
    HECTARE: "hectare"
    ACRE: "acre"
    SQUARE_FOOT: "sqft"

    def get_display_name(self):
        names = {
            "m2": "Square Meter (m²)",
            "km2": "Square Kilometer (km²)",
            "hectare": "Hectare (ha)",
            "acre": "Acre (ac)",
            "sqft": "Square Foot (ft²)"
        }

        return names[self.value]