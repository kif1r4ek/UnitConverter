"""
Unit tests for weight conversion service.

Tests cover:
- Basic weight conversions (mg, g, kg, ton, oz, lb, stone, ton_us)
- Edge cases (zero values, very large/small numbers)
- Decimal rounding
- Exception handling
"""
import pytest
from app.services.weight import convert_weight
from app.domain.units.weight import UnitsWeight
from app.domain.exceptions import (
    UnsupportedUnitError,
    DimensionalityConversionError,
    ConversionError
)


@pytest.mark.unit
class TestWeightConversions:
    """Test basic weight unit conversions."""

    def test_kilograms_to_grams(self):
        """Test conversion from kilograms to grams."""
        result = convert_weight(1, UnitsWeight.KILOGRAM, UnitsWeight.GRAM)
        assert result == 1000.0

    def test_grams_to_milligrams(self):
        """Test conversion from grams to milligrams."""
        result = convert_weight(1, UnitsWeight.GRAM, UnitsWeight.MILLIGRAM)
        assert result == 1000.0

    def test_kilograms_to_tons(self):
        """Test conversion from kilograms to metric tons."""
        result = convert_weight(1000, UnitsWeight.KILOGRAM, UnitsWeight.TON)
        assert result == 1.0

    def test_kilograms_to_pounds(self):
        """Test conversion from kilograms to pounds."""
        result = convert_weight(1, UnitsWeight.KILOGRAM, UnitsWeight.POUND)
        assert result == 2.2

    def test_pounds_to_kilograms(self):
        """Test conversion from pounds to kilograms."""
        result = convert_weight(1, UnitsWeight.POUND, UnitsWeight.KILOGRAM)
        assert result == 0.45

    def test_pounds_to_ounces(self):
        """Test conversion from pounds to ounces."""
        result = convert_weight(1, UnitsWeight.POUND, UnitsWeight.OUNCE)
        assert result == 16.0

    def test_ounces_to_grams(self):
        """Test conversion from ounces to grams."""
        result = convert_weight(1, UnitsWeight.OUNCE, UnitsWeight.GRAM)
        assert result == 28.35

    def test_stone_to_pounds(self):
        """Test conversion from stone to pounds."""
        result = convert_weight(1, UnitsWeight.STONE, UnitsWeight.POUND)
        assert result == 14.0

    def test_stone_to_kilograms(self):
        """Test conversion from stone to kilograms."""
        result = convert_weight(1, UnitsWeight.STONE, UnitsWeight.KILOGRAM)
        assert result == 6.35

    def test_ton_us_to_kilograms(self):
        """Test conversion from US ton to kilograms."""
        result = convert_weight(1, UnitsWeight.TON_US, UnitsWeight.KILOGRAM)
        assert result == 907.18


@pytest.mark.unit
class TestDecimalRounding:
    """Test decimal rounding behavior."""

    def test_default_two_decimals(self):
        """Test default rounding to 2 decimal places."""
        result = convert_weight(1, UnitsWeight.KILOGRAM, UnitsWeight.POUND)
        assert result == 2.2

    def test_custom_decimal_places_zero(self):
        """Test rounding to 0 decimal places."""
        result = convert_weight(1.567, UnitsWeight.KILOGRAM, UnitsWeight.GRAM, decimals=0)
        assert result == 1567.0

    def test_custom_decimal_places_four(self):
        """Test rounding to 4 decimal places."""
        result = convert_weight(1, UnitsWeight.KILOGRAM, UnitsWeight.POUND, decimals=4)
        assert result == 2.2046

    def test_custom_decimal_places_six(self):
        """Test rounding to 6 decimal places."""
        result = convert_weight(1, UnitsWeight.POUND, UnitsWeight.KILOGRAM, decimals=6)
        assert result == 0.453592


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and boundary values."""

    def test_zero_value(self):
        """Test conversion of zero value."""
        result = convert_weight(0, UnitsWeight.KILOGRAM, UnitsWeight.POUND)
        assert result == 0.0

    def test_very_large_value(self):
        """Test conversion of very large values."""
        result = convert_weight(1000000, UnitsWeight.KILOGRAM, UnitsWeight.TON)
        assert result == 1000.0

    def test_very_small_value(self):
        """Test conversion of very small values."""
        result = convert_weight(0.001, UnitsWeight.GRAM, UnitsWeight.MILLIGRAM)
        assert result == 1.0

    def test_fractional_value(self):
        """Test conversion of fractional values."""
        result = convert_weight(1.5, UnitsWeight.KILOGRAM, UnitsWeight.GRAM)
        assert result == 1500.0

    def test_same_unit_conversion(self):
        """Test converting between same units."""
        result = convert_weight(100, UnitsWeight.KILOGRAM, UnitsWeight.KILOGRAM)
        assert result == 100.0

    def test_negative_value_allowed(self):
        """Test that negative values are allowed for weight calculations."""
        result = convert_weight(-10, UnitsWeight.KILOGRAM, UnitsWeight.GRAM)
        assert result == -10000.0


@pytest.mark.unit
class TestPrecisionAndAccuracy:
    """Test precision and accuracy of conversions."""

    def test_kilograms_to_pounds_precision(self):
        """Test precise kg to lb conversion."""
        # 1 kg = 2.20462262 lb
        result = convert_weight(1, UnitsWeight.KILOGRAM, UnitsWeight.POUND, decimals=6)
        assert result == 2.204623

    def test_ounces_to_grams_precision(self):
        """Test precise oz to g conversion."""
        # 1 oz = 28.349523125 g
        result = convert_weight(1, UnitsWeight.OUNCE, UnitsWeight.GRAM, decimals=6)
        assert result == 28.349523

    def test_round_trip_conversion(self):
        """Test that round-trip conversion returns original value."""
        original = 42.5
        # kg -> lb -> kg
        to_lb = convert_weight(original, UnitsWeight.KILOGRAM, UnitsWeight.POUND, decimals=10)
        back_to_kg = convert_weight(to_lb, UnitsWeight.POUND, UnitsWeight.KILOGRAM, decimals=10)
        assert abs(back_to_kg - original) < 0.0001

    def test_round_trip_metric_imperial(self):
        """Test round-trip between metric and imperial."""
        original = 100.0
        # g -> oz -> g
        to_oz = convert_weight(original, UnitsWeight.GRAM, UnitsWeight.OUNCE, decimals=10)
        back_to_g = convert_weight(to_oz, UnitsWeight.OUNCE, UnitsWeight.GRAM, decimals=10)
        assert abs(back_to_g - original) < 0.0001


@pytest.mark.unit
class TestRealWorldScenarios:
    """Test real-world conversion scenarios."""

    def test_person_weight_kg_to_pounds(self):
        """Test converting person weight (70kg to lb)."""
        result = convert_weight(70, UnitsWeight.KILOGRAM, UnitsWeight.POUND)
        assert result == 154.32

    def test_person_weight_stone(self):
        """Test converting person weight (70kg to stone)."""
        result = convert_weight(70, UnitsWeight.KILOGRAM, UnitsWeight.STONE)
        assert result == 11.02

    def test_recipe_ingredient_grams_to_ounces(self):
        """Test converting recipe ingredient (250g to oz)."""
        result = convert_weight(250, UnitsWeight.GRAM, UnitsWeight.OUNCE)
        assert result == 8.82

    def test_shipping_weight(self):
        """Test converting shipping weight (5kg to lb)."""
        result = convert_weight(5, UnitsWeight.KILOGRAM, UnitsWeight.POUND)
        assert result == 11.02

    def test_large_cargo(self):
        """Test converting large cargo (2 metric tons to kg)."""
        result = convert_weight(2, UnitsWeight.TON, UnitsWeight.KILOGRAM)
        assert result == 2000.0

    def test_precious_metal(self):
        """Test converting precious metal (1 oz to grams)."""
        result = convert_weight(1, UnitsWeight.OUNCE, UnitsWeight.GRAM)
        assert result == 28.35

    def test_medication_dosage(self):
        """Test converting medication dosage (500mg to g)."""
        result = convert_weight(500, UnitsWeight.MILLIGRAM, UnitsWeight.GRAM)
        assert result == 0.5


@pytest.mark.unit
class TestMetricToImperial:
    """Test various metric to imperial conversions."""

    def test_gram_to_ounce(self):
        """Test g to oz conversion."""
        result = convert_weight(100, UnitsWeight.GRAM, UnitsWeight.OUNCE)
        assert result == 3.53

    def test_kilogram_to_stone(self):
        """Test kg to stone conversion."""
        result = convert_weight(50, UnitsWeight.KILOGRAM, UnitsWeight.STONE)
        assert result == 7.87

    def test_ton_to_ton_us(self):
        """Test metric ton to US ton conversion."""
        result = convert_weight(1, UnitsWeight.TON, UnitsWeight.TON_US)
        assert result == 1.1


@pytest.mark.unit
class TestImperialToMetric:
    """Test various imperial to metric conversions."""

    def test_pound_to_gram(self):
        """Test lb to g conversion."""
        result = convert_weight(1, UnitsWeight.POUND, UnitsWeight.GRAM)
        assert result == 453.59

    def test_ounce_to_milligram(self):
        """Test oz to mg conversion."""
        result = convert_weight(1, UnitsWeight.OUNCE, UnitsWeight.MILLIGRAM)
        assert result == 28349.52

    def test_stone_to_gram(self):
        """Test stone to g conversion."""
        result = convert_weight(1, UnitsWeight.STONE, UnitsWeight.GRAM)
        assert result == 6350.29
