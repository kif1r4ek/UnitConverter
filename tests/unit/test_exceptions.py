"""
Unit tests for custom exceptions.

Tests cover:
- ConversionError base class
- UnsupportedUnitError
- InvalidValueError
- DimensionalityConversionError
- NegativeValueError
"""
import pytest
from app.domain.exceptions import (
    ConversionError,
    UnsupportedUnitError,
    InvalidValueError,
    DimensionalityConversionError,
    NegativeValueError
)


@pytest.mark.unit
class TestConversionError:
    """Test base ConversionError exception."""

    def test_conversion_error_creation(self):
        """Test creating ConversionError with message."""
        error = ConversionError("Test error message")
        assert str(error) == "Test error message"

    def test_conversion_error_inheritance(self):
        """Test that ConversionError inherits from Exception."""
        error = ConversionError("Test")
        assert isinstance(error, Exception)

    def test_conversion_error_can_be_raised(self):
        """Test that ConversionError can be raised and caught."""
        with pytest.raises(ConversionError) as exc_info:
            raise ConversionError("Test conversion error")
        assert "Test conversion error" in str(exc_info.value)


@pytest.mark.unit
class TestUnsupportedUnitError:
    """Test UnsupportedUnitError exception."""

    def test_unsupported_unit_error_creation(self):
        """Test creating UnsupportedUnitError with unit name."""
        error = UnsupportedUnitError("parsec")
        assert error.unit == "parsec"
        assert "Unsupported unit: 'parsec'" in str(error)

    def test_unsupported_unit_error_inheritance(self):
        """Test that UnsupportedUnitError inherits from ConversionError."""
        error = UnsupportedUnitError("furlong")
        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)

    def test_unsupported_unit_error_message_format(self):
        """Test the error message format."""
        error = UnsupportedUnitError("invalid_unit")
        assert str(error) == "Unsupported unit: 'invalid_unit'"

    def test_unsupported_unit_error_can_be_raised(self):
        """Test that error can be raised and caught."""
        with pytest.raises(UnsupportedUnitError) as exc_info:
            raise UnsupportedUnitError("unknown")
        assert exc_info.value.unit == "unknown"


@pytest.mark.unit
class TestInvalidValueError:
    """Test InvalidValueError exception."""

    def test_invalid_value_error_creation(self):
        """Test creating InvalidValueError with message."""
        error = InvalidValueError("Value must be a number")
        assert str(error) == "Value must be a number"

    def test_invalid_value_error_inheritance(self):
        """Test that InvalidValueError inherits from ConversionError."""
        error = InvalidValueError("Test")
        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)

    def test_invalid_value_error_can_be_raised(self):
        """Test that error can be raised and caught."""
        with pytest.raises(InvalidValueError) as exc_info:
            raise InvalidValueError("Invalid input")
        assert "Invalid input" in str(exc_info.value)


@pytest.mark.unit
class TestDimensionalityConversionError:
    """Test DimensionalityConversionError exception."""

    def test_dimensionality_error_creation(self):
        """Test creating DimensionalityConversionError with units."""
        error = DimensionalityConversionError("meter", "degC")
        assert error.from_unit == "meter"
        assert error.to_unit == "degC"
        assert "Cannot convert between incompatible units: 'meter' to 'degC'" in str(error)

    def test_dimensionality_error_inheritance(self):
        """Test that DimensionalityConversionError inherits from ConversionError."""
        error = DimensionalityConversionError("m", "kg")
        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)

    def test_dimensionality_error_message_format(self):
        """Test the error message format."""
        error = DimensionalityConversionError("kilometer", "pound")
        expected = "Cannot convert between incompatible units: 'kilometer' to 'pound'"
        assert str(error) == expected

    def test_dimensionality_error_attributes(self):
        """Test that error stores from_unit and to_unit."""
        error = DimensionalityConversionError("cm", "liter")
        assert error.from_unit == "cm"
        assert error.to_unit == "liter"

    def test_dimensionality_error_can_be_raised(self):
        """Test that error can be raised and caught."""
        with pytest.raises(DimensionalityConversionError) as exc_info:
            raise DimensionalityConversionError("meter", "second")
        assert exc_info.value.from_unit == "meter"
        assert exc_info.value.to_unit == "second"


@pytest.mark.unit
class TestNegativeValueError:
    """Test NegativeValueError exception."""

    def test_negative_value_error_creation(self):
        """Test creating NegativeValueError with unit type."""
        error = NegativeValueError("weight")
        assert error.unit_type == "weight"
        assert "Negative values are not allowed for weight" in str(error)

    def test_negative_value_error_inheritance(self):
        """Test that NegativeValueError inherits from InvalidValueError."""
        error = NegativeValueError("length")
        assert isinstance(error, InvalidValueError)
        assert isinstance(error, ConversionError)
        assert isinstance(error, Exception)

    def test_negative_value_error_message_format(self):
        """Test the error message format."""
        error = NegativeValueError("distance")
        assert str(error) == "Negative values are not allowed for distance"

    def test_negative_value_error_attributes(self):
        """Test that error stores unit_type."""
        error = NegativeValueError("mass")
        assert error.unit_type == "mass"

    def test_negative_value_error_can_be_raised(self):
        """Test that error can be raised and caught."""
        with pytest.raises(NegativeValueError) as exc_info:
            raise NegativeValueError("conversion value")
        assert exc_info.value.unit_type == "conversion value"


@pytest.mark.unit
class TestExceptionHierarchy:
    """Test exception inheritance hierarchy."""

    def test_all_conversion_errors_inherit_from_base(self):
        """Test that all custom exceptions inherit from ConversionError."""
        exceptions = [
            UnsupportedUnitError("test"),
            InvalidValueError("test"),
            DimensionalityConversionError("a", "b"),
            NegativeValueError("test")
        ]

        for exc in exceptions:
            assert isinstance(exc, ConversionError)

    def test_catch_base_exception(self):
        """Test that base ConversionError can catch all child exceptions."""
        with pytest.raises(ConversionError):
            raise UnsupportedUnitError("test")

        with pytest.raises(ConversionError):
            raise InvalidValueError("test")

        with pytest.raises(ConversionError):
            raise DimensionalityConversionError("a", "b")

        with pytest.raises(ConversionError):
            raise NegativeValueError("test")

    def test_specific_exception_catching(self):
        """Test catching specific exception types."""
        with pytest.raises(UnsupportedUnitError):
            raise UnsupportedUnitError("test")

        with pytest.raises(DimensionalityConversionError):
            raise DimensionalityConversionError("a", "b")

        with pytest.raises(NegativeValueError):
            raise NegativeValueError("test")
