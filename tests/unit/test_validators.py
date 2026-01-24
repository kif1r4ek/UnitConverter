"""
Unit tests for domain validators.

Tests cover:
- PositiveValueValidator for length/weight
- Pydantic field validation
- Custom exception raising
"""
import pytest
from pydantic import ValidationError
from app.domain.models.validator import PositiveValueValidator
from app.domain.exceptions import NegativeValueError


@pytest.mark.unit
class TestPositiveValueValidator:
    """Test PositiveValueValidator for ensuring non-negative values."""

    def test_positive_value_accepted(self):
        """Test that positive values are accepted."""
        validator = PositiveValueValidator(value=100.0, decimals=2)
        assert validator.value == 100.0

    def test_zero_value_accepted(self):
        """Test that zero value is accepted."""
        validator = PositiveValueValidator(value=0.0, decimals=2)
        assert validator.value == 0.0

    def test_large_positive_value_accepted(self):
        """Test that large positive values are accepted."""
        validator = PositiveValueValidator(value=999999999.99, decimals=2)
        assert validator.value == 999999999.99

    def test_small_positive_value_accepted(self):
        """Test that small positive values are accepted."""
        validator = PositiveValueValidator(value=0.001, decimals=2)
        assert validator.value == 0.001

    def test_negative_value_raises_error(self):
        """Test that negative values raise error via ValidationError."""
        with pytest.raises((ValidationError, NegativeValueError)):
            PositiveValueValidator(value=-10.0, decimals=2)

    def test_negative_small_value_raises_error(self):
        """Test that small negative values raise error."""
        with pytest.raises((ValidationError, NegativeValueError)):
            PositiveValueValidator(value=-0.001, decimals=2)

    def test_negative_large_value_raises_error(self):
        """Test that large negative values raise error."""
        with pytest.raises((ValidationError, NegativeValueError)):
            PositiveValueValidator(value=-999999.99, decimals=2)

    def test_decimals_field_validation(self):
        """Test that decimals field accepts valid values."""
        validator = PositiveValueValidator(value=100.0, decimals=0)
        assert validator.decimals == 0

        validator = PositiveValueValidator(value=100.0, decimals=10)
        assert validator.decimals == 10

    def test_decimals_defaults_to_two(self):
        """Test that decimals defaults to 2 when not provided."""
        validator = PositiveValueValidator(value=100.0)
        assert validator.decimals == 2
