from enum import Enum



class UnitsWeight(Enum):
    MILLIGRAM = "mg"
    GRAM = "g"
    KILOGRAM = "kg"
    TON = "ton"
    OUNCE = "oz"
    POUND = "lb"
    STONE = "stone"
    TON_US = "ton_us"

    def get_display_name(self):

        names = {
            "mg": "Milligram (mg)",
            "g": "Gram (g)",
            "kg": "Kilogram (kg)",
            "ton": "Metric Ton (t)",
            "oz": "Ounce (oz)",
            "lb": "Pound (lb)",
            "stone": "Stone (st)",
            "ton_us": "US Ton",
        }

        return names[self.value]