from enum import Enum


class UnitsLength(str, Enum):
    MILLIMETER = "mm"
    CENTIMETER = "cm"
    METER = "m"
    KILOMETER = "km"
    INCH = "inch"
    FOOT = "foot"
    YARD = "yard"
    MILE = "mile"
    SQUARE_METER = "m2"
    SQUARE_KILOMETER = "km2"
    HECTARE = "hectare"
    ACRE = "acre"
    SQUARE_FOOT = "sqft"


UNITS_LENGTH_MAPPING: dict[UnitsLength, str] = {
    UnitsLength.MILLIMETER: "millimeter",
    UnitsLength.CENTIMETER: "centimeter",
    UnitsLength.METER: "meter",
    UnitsLength.KILOMETER: "kilometer",
    UnitsLength.INCH: "inch",
    UnitsLength.FOOT: "foot",
    UnitsLength.YARD: "yard",
    UnitsLength.MILE: "mile",
    UnitsLength.SQUARE_METER: "meter**2",
    UnitsLength.SQUARE_KILOMETER: "kilometer**2",
    UnitsLength.HECTARE: "hectare",
    UnitsLength.ACRE: "acre",
    UnitsLength.SQUARE_FOOT: "square_foot",
}
