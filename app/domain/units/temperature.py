from enum import Enum


class UnitsTemperature(str, Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"


UNITS_TEMPERATURE_MAPPING: dict[UnitsTemperature, str] = {
    UnitsTemperature.CELSIUS: "degC",
    UnitsTemperature.FAHRENHEIT: "degF",
    UnitsTemperature.KELVIN: "kelvin"
}

