from enum import Enum


class UnitsWeight(str, Enum):
    MILLIGRAM = "mg"
    GRAM = "g"
    KILOGRAM = "kg"
    TON = "ton"
    OUNCE = "oz"
    POUND = "lb"
    STONE = "stone"
    TON_US = "ton_us"


UNITS_WEIGHT_MAPPING: dict[UnitsWeight, str] = {
    UnitsWeight.MILLIGRAM: "milligram",
    UnitsWeight.GRAM: "gram",
    UnitsWeight.KILOGRAM: "kilogram",
    UnitsWeight.TON: "tonne",
    UnitsWeight.OUNCE: "ounce",
    UnitsWeight.POUND: "pound",
    UnitsWeight.STONE: "stone",
    UnitsWeight.TON_US: "short_ton",
}