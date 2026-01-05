from pint import UnitRegistry

ureg = UnitRegistry()

UNITS_TEMPERATURE_MAPPING = {
    "celsius": "degC",
    "fahrenheit": "degF",
    "kelvin": "kelvin"
}

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    try:
        from_unit = UNITS_TEMPERATURE_MAPPING[from_unit]
        to_unit = UNITS_TEMPERATURE_MAPPING[to_unit]

        quantity = ureg.Quantity(value, from_unit)
        result = quantity.to(to_unit)

    except Exception as e:
        # Позже здесь будет logger
        raise ValueError(f"Conversion error: {str(e)}")

    return round(result.magnitude, 2)





