"""
Unit tests for length conversion service.

Tests cover:
- Basic linear conversions (m, cm, km, inch, foot, yard, mile)
- Area conversions (m2, km2, hectare, acre, sqft)
- Edge cases (zero values, very large/small numbers)
- Decimal rounding
- Exception handling
"""
import pytest
from app.services.length import convert_length
from app.domain.units.length import UnitsLength
from app.domain.exceptions import (
    UnsupportedUnitError,
    DimensionalityConversionError,
    ConversionError
)


@pytest.mark.unit
class TestLengthConversions:
    """Test basic length unit conversions."""

    def test_meters_to_kilometers(self):
        """Test conversion from meters to kilometers."""
        result = convert_length(1000, UnitsLength.METER, UnitsLength.KILOMETER)
        assert result == 1.0

    def test_meters_to_centimeters(self):
        """Test conversion from meters to centimeters."""
        result = convert_length(1, UnitsLength.METER, UnitsLength.CENTIMETER)
        assert result == 100.0

    def test_meters_to_millimeters(self):
        """Test conversion from meters to millimeters."""
        result = convert_length(1, UnitsLength.METER, UnitsLength.MILLIMETER)
        assert result == 1000.0

    def test_kilometers_to_meters(self):
        """Test conversion from kilometers to meters."""
        result = convert_length(1.5, UnitsLength.KILOMETER, UnitsLength.METER)
        assert result == 1500.0

    def test_inches_to_centimeters(self):
        """Test conversion from inches to centimeters."""
        result = convert_length(1, UnitsLength.INCH, UnitsLength.CENTIMETER)
        assert result == 2.54

    def test_feet_to_meters(self):
        """Test conversion from feet to meters."""
        result = convert_length(1, UnitsLength.FOOT, UnitsLength.METER)
        assert result == 0.3

    def test_yards_to_meters(self):
        """Test conversion from yards to meters."""
        result = convert_length(1, UnitsLength.YARD, UnitsLength.METER)
        assert result == 0.91

    def test_miles_to_kilometers(self):
        """Test conversion from miles to kilometers."""
        result = convert_length(1, UnitsLength.MILE, UnitsLength.KILOMETER)
        assert result == 1.61

    def test_miles_to_feet(self):
        """Test conversion from miles to feet."""
        result = convert_length(1, UnitsLength.MILE, UnitsLength.FOOT)
        assert result == 5280.0


@pytest.mark.unit
class TestAreaConversions:
    """Test area unit conversions."""

    def test_square_meters_to_square_kilometers(self):
        """Test conversion from m² to km²."""
        result = convert_length(1000000, UnitsLength.SQUARE_METER, UnitsLength.SQUARE_KILOMETER)
        assert result == 1.0

    def test_hectare_to_square_meters(self):
        """Test conversion from hectare to m²."""
        result = convert_length(1, UnitsLength.HECTARE, UnitsLength.SQUARE_METER)
        assert result == 10000.0

    def test_acre_to_square_feet(self):
        """Test conversion from acre to sqft."""
        result = convert_length(1, UnitsLength.ACRE, UnitsLength.SQUARE_FOOT)
        assert result == 43560.17

    def test_square_feet_to_square_meters(self):
        """Test conversion from sqft to m²."""
        result = convert_length(1, UnitsLength.SQUARE_FOOT, UnitsLength.SQUARE_METER)
        assert result == 0.09

    def test_square_kilometers_to_hectares(self):
        """Test conversion from km² to hectares."""
        result = convert_length(1, UnitsLength.SQUARE_KILOMETER, UnitsLength.HECTARE)
        assert result == 100.0


@pytest.mark.unit
class TestDecimalRounding:
    """Test decimal rounding behavior."""

    def test_default_two_decimals(self):
        """Test default rounding to 2 decimal places."""
        result = convert_length(1, UnitsLength.METER, UnitsLength.FOOT)
        assert result == 3.28

    def test_custom_decimal_places_zero(self):
        """Test rounding to 0 decimal places."""
        result = convert_length(1.567, UnitsLength.METER, UnitsLength.CENTIMETER, decimals=0)
        assert result == 157.0

    def test_custom_decimal_places_four(self):
        """Test rounding to 4 decimal places."""
        result = convert_length(1, UnitsLength.METER, UnitsLength.FOOT, decimals=4)
        assert result == 3.2808

    def test_custom_decimal_places_six(self):
        """Test rounding to 6 decimal places."""
        result = convert_length(1, UnitsLength.MILE, UnitsLength.KILOMETER, decimals=6)
        assert result == 1.609344


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases and boundary values."""

    def test_zero_value(self):
        """Test conversion of zero value."""
        result = convert_length(0, UnitsLength.METER, UnitsLength.KILOMETER)
        assert result == 0.0

    def test_very_large_value(self):
        """Test conversion of very large values."""
        result = convert_length(1000000000, UnitsLength.METER, UnitsLength.KILOMETER)
        assert result == 1000000.0

    def test_very_small_value(self):
        """Test conversion of very small values."""
        result = convert_length(0.001, UnitsLength.METER, UnitsLength.MILLIMETER)
        assert result == 1.0

    def test_fractional_value(self):
        """Test conversion of fractional values."""
        result = convert_length(1.5, UnitsLength.METER, UnitsLength.CENTIMETER)
        assert result == 150.0

    def test_same_unit_conversion(self):
        """Test converting between same units."""
        result = convert_length(100, UnitsLength.METER, UnitsLength.METER)
        assert result == 100.0

    def test_negative_value_allowed(self):
        """Test that negative values are allowed for length (relative positions)."""
        result = convert_length(-10, UnitsLength.METER, UnitsLength.CENTIMETER)
        assert result == -1000.0


@pytest.mark.unit
class TestDimensionalityErrors:
    """Test dimensionality conversion errors."""

    def test_linear_to_area_raises_error(self):
        """Test that converting linear to area raises error."""
        with pytest.raises(DimensionalityConversionError) as exc_info:
            convert_length(100, UnitsLength.METER, UnitsLength.SQUARE_METER)

        assert "Cannot convert between incompatible units" in str(exc_info.value)
        assert exc_info.value.from_unit == "meter"
        assert exc_info.value.to_unit == "meter**2"

    def test_area_to_linear_raises_error(self):
        """Test that converting area to linear raises error."""
        with pytest.raises(DimensionalityConversionError) as exc_info:
            convert_length(100, UnitsLength.SQUARE_METER, UnitsLength.METER)

        assert "Cannot convert between incompatible units" in str(exc_info.value)


@pytest.mark.unit
class TestPrecisionAndAccuracy:
    """Test precision and accuracy of conversions."""

    def test_meters_to_feet_precision(self):
        """Test precise meter to feet conversion."""
        # 1 meter = 3.280839895 feet
        result = convert_length(1, UnitsLength.METER, UnitsLength.FOOT, decimals=6)
        assert result == 3.28084

    def test_inches_to_centimeters_precision(self):
        """Test precise inch to cm conversion."""
        # 1 inch = 2.54 cm (exact)
        result = convert_length(1, UnitsLength.INCH, UnitsLength.CENTIMETER, decimals=6)
        assert result == 2.54

    def test_round_trip_conversion(self):
        """Test that round-trip conversion returns original value."""
        original = 42.5
        # m -> km -> m
        to_km = convert_length(original, UnitsLength.METER, UnitsLength.KILOMETER, decimals=10)
        back_to_m = convert_length(to_km, UnitsLength.KILOMETER, UnitsLength.METER, decimals=10)
        assert abs(back_to_m - original) < 0.0001

    def test_round_trip_imperial_metric(self):
        """Test round-trip between imperial and metric."""
        original = 100.0
        # m -> feet -> m
        to_feet = convert_length(original, UnitsLength.METER, UnitsLength.FOOT, decimals=10)
        back_to_m = convert_length(to_feet, UnitsLength.FOOT, UnitsLength.METER, decimals=10)
        assert abs(back_to_m - original) < 0.0001


@pytest.mark.unit
class TestRealWorldScenarios:
    """Test real-world conversion scenarios."""

    def test_athletic_track_distance(self):
        """Test converting athletic track distance (400m to yards)."""
        result = convert_length(400, UnitsLength.METER, UnitsLength.YARD)
        assert result == 437.45

    def test_building_height(self):
        """Test converting building height (100m to feet)."""
        result = convert_length(100, UnitsLength.METER, UnitsLength.FOOT)
        assert result == 328.08

    def test_land_area(self):
        """Test converting land area (1 hectare to acres)."""
        result = convert_length(1, UnitsLength.HECTARE, UnitsLength.ACRE)
        assert result == 2.47

    def test_road_distance(self):
        """Test converting road distance (50 miles to km)."""
        result = convert_length(50, UnitsLength.MILE, UnitsLength.KILOMETER)
        assert result == 80.47

    def test_room_dimensions(self):
        """Test converting room dimensions (15 feet to meters)."""
        result = convert_length(15, UnitsLength.FOOT, UnitsLength.METER)
        assert result == 4.57
