from enum import Enum
from os import name


class UnitsTemperature(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"

    def get_display_name(self):

        names = {
            "celsius": "Celsius (°C)",
            "fahrenheit": "Fahrenheit (°F)",
            "kelvin": "Kelvin (K)",
        }

        return names[self.value]