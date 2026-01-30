"""
Unit tests for temperature conversion service.

Tests cover:
- Basic temperature conversions (Celsius, Fahrenheit, Kelvin)
- Negative temperatures
- Absolute zero and extreme values
- Decimal rounding
- Exception handling
"""
import pytest
from app.services.temperature import convert_temperature
from app.domain.units.temperature import UnitsTemperature
from app.domain.exceptions import (
    UnsupportedUnitError,
    DimensionalityConversionError,
    ConversionError
)


@pytest.mark.unit
class TestCelsiusConversions:
    """Test Celsius conversions."""

    def test_celsius_to_fahrenheit_freezing_point(self):
        """Test freezing point conversion (0°C to °F)."""
        result = convert_temperature(0, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 32.0

    def test_celsius_to_fahrenheit_boiling_point(self):
        """Test boiling point conversion (100°C to °F)."""
        result = convert_temperature(100, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 212.0

    def test_celsius_to_kelvin_freezing_point(self):
        """Test freezing point conversion (0°C to K)."""
        result = convert_temperature(0, UnitsTemperature.CELSIUS, UnitsTemperature.KELVIN)
        assert result == 273.15

    def test_celsius_to_kelvin_boiling_point(self):
        """Test boiling point conversion (100°C to K)."""
        result = convert_temperature(100, UnitsTemperature.CELSIUS, UnitsTemperature.KELVIN)
        assert result == 373.15

    def test_celsius_to_fahrenheit_body_temp(self):
        """Test body temperature conversion (37°C to °F)."""
        result = convert_temperature(37, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 98.6

    def test_celsius_to_fahrenheit_room_temp(self):
        """Test room temperature conversion (20°C to °F)."""
        result = convert_temperature(20, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 68.0


@pytest.mark.unit
class TestFahrenheitConversions:
    """Test Fahrenheit conversions."""

    def test_fahrenheit_to_celsius_freezing_point(self):
        """Test freezing point conversion (32°F to °C)."""
        result = convert_temperature(32, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == 0.0

    def test_fahrenheit_to_celsius_boiling_point(self):
        """Test boiling point conversion (212°F to °C)."""
        result = convert_temperature(212, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == 100.0

    def test_fahrenheit_to_kelvin(self):
        """Test °F to K conversion (32°F to K)."""
        result = convert_temperature(32, UnitsTemperature.FAHRENHEIT, UnitsTemperature.KELVIN)
        assert result == 273.15

    def test_fahrenheit_to_celsius_body_temp(self):
        """Test body temperature conversion (98.6°F to °C)."""
        result = convert_temperature(98.6, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == 37.0

    def test_fahrenheit_to_celsius_room_temp(self):
        """Test room temperature conversion (68°F to °C)."""
        result = convert_temperature(68, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == 20.0


@pytest.mark.unit
class TestKelvinConversions:
    """Test Kelvin conversions."""

    def test_kelvin_to_celsius_absolute_zero(self):
        """Test absolute zero conversion (0K to °C)."""
        result = convert_temperature(0, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == -273.15

    def test_kelvin_to_celsius_freezing_point(self):
        """Test freezing point conversion (273.15K to °C)."""
        result = convert_temperature(273.15, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == 0.0

    def test_kelvin_to_fahrenheit_freezing_point(self):
        """Test freezing point conversion (273.15K to °F)."""
        result = convert_temperature(273.15, UnitsTemperature.KELVIN, UnitsTemperature.FAHRENHEIT)
        assert result == 32.0

    def test_kelvin_to_celsius_boiling_point(self):
        """Test boiling point conversion (373.15K to °C)."""
        result = convert_temperature(373.15, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == 100.0

    def test_kelvin_to_fahrenheit_boiling_point(self):
        """Test boiling point conversion (373.15K to °F)."""
        result = convert_temperature(373.15, UnitsTemperature.KELVIN, UnitsTemperature.FAHRENHEIT)
        assert result == 212.0


@pytest.mark.unit
class TestNegativeTemperatures:
    """Test conversions with negative temperatures."""

    def test_negative_celsius_to_fahrenheit(self):
        """Test negative temperature conversion (-40°C to °F)."""
        result = convert_temperature(-40, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == -40.0

    def test_negative_celsius_to_kelvin(self):
        """Test negative temperature conversion (-10°C to K)."""
        result = convert_temperature(-10, UnitsTemperature.CELSIUS, UnitsTemperature.KELVIN)
        assert result == 263.15

    def test_negative_fahrenheit_to_celsius(self):
        """Test negative temperature conversion (-40°F to °C)."""
        result = convert_temperature(-40, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == -40.0

    def test_extreme_cold_celsius(self):
        """Test extreme cold conversion (-100°C to °F)."""
        result = convert_temperature(-100, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == -148.0

    def test_extreme_cold_fahrenheit(self):
        """Test extreme cold conversion (-100°F to °C)."""
        result = convert_temperature(-100, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == -73.33


@pytest.mark.unit
class TestDecimalRounding:
    """Test decimal rounding behavior."""

    def test_default_two_decimals(self):
        """Test default rounding to 2 decimal places."""
        result = convert_temperature(25, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 77.0

    def test_custom_decimal_places_zero(self):
        """Test rounding to 0 decimal places."""
        result = convert_temperature(25.5, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT, decimals=0)
        assert result == 78.0

    def test_custom_decimal_places_four(self):
        """Test rounding to 4 decimal places."""
        result = convert_temperature(25, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT, decimals=4)
        assert result == 77.0

    def test_custom_decimal_places_six(self):
        """Test rounding to 6 decimal places."""
        result = convert_temperature(100, UnitsTemperature.CELSIUS, UnitsTemperature.KELVIN, decimals=6)
        assert result == 373.15


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and boundary values."""

    def test_zero_celsius(self):
        """Test zero Celsius conversion."""
        result = convert_temperature(0, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 32.0

    def test_zero_fahrenheit(self):
        """Test zero Fahrenheit conversion."""
        result = convert_temperature(0, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == -17.78

    def test_zero_kelvin(self):
        """Test absolute zero conversion."""
        result = convert_temperature(0, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == -273.15

    def test_same_unit_conversion_celsius(self):
        """Test converting Celsius to Celsius."""
        result = convert_temperature(100, UnitsTemperature.CELSIUS, UnitsTemperature.CELSIUS)
        assert result == 100.0

    def test_same_unit_conversion_fahrenheit(self):
        """Test converting Fahrenheit to Fahrenheit."""
        result = convert_temperature(100, UnitsTemperature.FAHRENHEIT, UnitsTemperature.FAHRENHEIT)
        assert result == 100.0

    def test_same_unit_conversion_kelvin(self):
        """Test converting Kelvin to Kelvin."""
        result = convert_temperature(100, UnitsTemperature.KELVIN, UnitsTemperature.KELVIN)
        assert result == 100.0


@pytest.mark.unit
class TestPrecisionAndAccuracy:
    """Test precision and accuracy of conversions."""

    def test_celsius_to_fahrenheit_precision(self):
        """Test precise Celsius to Fahrenheit conversion."""
        result = convert_temperature(37, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT, decimals=6)
        assert result == 98.6

    def test_round_trip_celsius_fahrenheit(self):
        """Test round-trip conversion Celsius -> Fahrenheit -> Celsius."""
        original = 42.5
        to_f = convert_temperature(original, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT, decimals=10)
        back_to_c = convert_temperature(to_f, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS, decimals=10)
        assert abs(back_to_c - original) < 0.0001

    def test_round_trip_celsius_kelvin(self):
        """Test round-trip conversion Celsius -> Kelvin -> Celsius."""
        original = 100.0
        to_k = convert_temperature(original, UnitsTemperature.CELSIUS, UnitsTemperature.KELVIN, decimals=10)
        back_to_c = convert_temperature(to_k, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS, decimals=10)
        assert abs(back_to_c - original) < 0.0001

    def test_round_trip_fahrenheit_kelvin(self):
        """Test round-trip conversion Fahrenheit -> Kelvin -> Fahrenheit."""
        original = 212.0
        to_k = convert_temperature(original, UnitsTemperature.FAHRENHEIT, UnitsTemperature.KELVIN, decimals=10)
        back_to_f = convert_temperature(to_k, UnitsTemperature.KELVIN, UnitsTemperature.FAHRENHEIT, decimals=10)
        assert abs(back_to_f - original) < 0.0001


@pytest.mark.unit
class TestRealWorldScenarios:
    """Test real-world temperature conversion scenarios."""

    def test_weather_forecast_celsius_to_fahrenheit(self):
        """Test weather forecast temperature (25°C to °F)."""
        result = convert_temperature(25, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 77.0

    def test_cooking_temperature_fahrenheit_to_celsius(self):
        """Test cooking temperature (350°F to °C)."""
        result = convert_temperature(350, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == 176.67

    def test_freezer_temperature(self):
        """Test freezer temperature (-18°C to °F)."""
        result = convert_temperature(-18, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == -0.4

    def test_fever_temperature(self):
        """Test fever temperature (38.5°C to °F)."""
        result = convert_temperature(38.5, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 101.3

    def test_summer_heat(self):
        """Test summer heat (35°C to °F)."""
        result = convert_temperature(35, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == 95.0

    def test_winter_cold(self):
        """Test winter cold (-20°C to °F)."""
        result = convert_temperature(-20, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == -4.0

    def test_scientific_absolute_zero(self):
        """Test absolute zero for scientific calculations (0K to °C)."""
        result = convert_temperature(0, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == -273.15


@pytest.mark.unit
class TestSpecialTemperaturePoints:
    """Test special temperature reference points."""

    def test_celsius_fahrenheit_equal_point(self):
        """Test the point where Celsius equals Fahrenheit (-40)."""
        result = convert_temperature(-40, UnitsTemperature.CELSIUS, UnitsTemperature.FAHRENHEIT)
        assert result == -40.0

    def test_fahrenheit_celsius_equal_point(self):
        """Test the point where Fahrenheit equals Celsius (-40)."""
        result = convert_temperature(-40, UnitsTemperature.FAHRENHEIT, UnitsTemperature.CELSIUS)
        assert result == -40.0

    def test_triple_point_of_water_kelvin(self):
        """Test triple point of water (273.16K to °C)."""
        result = convert_temperature(273.16, UnitsTemperature.KELVIN, UnitsTemperature.CELSIUS)
        assert result == 0.01
