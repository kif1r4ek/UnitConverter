"""
Integration tests for error handlers.

Tests cover:
- ConversionError handling (400)
- ValidationError handling (422)
- Generic Exception handling (500)
- Error response format
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app.core.error_handlers import register_exception_handlers
from app.domain.exceptions import (
    ConversionError,
    UnsupportedUnitError,
    DimensionalityConversionError,
    NegativeValueError
)


@pytest.mark.integration
class TestConversionErrorHandler:
    """Test ConversionError exception handler."""

    @pytest.fixture
    def test_app(self):
        """Create test app with error handlers."""
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/test-conversion-error")
        async def trigger_conversion_error():
            raise ConversionError("Test conversion error")

        @app.get("/test-unsupported-unit")
        async def trigger_unsupported_unit():
            raise UnsupportedUnitError("parsec")

        @app.get("/test-dimensionality-error")
        async def trigger_dimensionality_error():
            raise DimensionalityConversionError("meter", "second")

        @app.get("/test-negative-value-error")
        async def trigger_negative_value():
            raise NegativeValueError("weight")

        return app

    @pytest.fixture
    def test_client(self, test_app):
        """Create test client."""
        return TestClient(test_app, raise_server_exceptions=False)

    def test_conversion_error_returns_400(self, test_client):
        """Test that ConversionError returns 400 status code."""
        response = test_client.get("/test-conversion-error")

        assert response.status_code == 400

    def test_conversion_error_response_format(self, test_client):
        """Test ConversionError response format."""
        response = test_client.get("/test-conversion-error")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "detail" in data
        assert "type" in data
        assert data["error"] == "ConversionError"
        assert data["detail"] == "Test conversion error"
        assert data["type"] == "ConversionError"

    def test_unsupported_unit_error_handled(self, test_client):
        """Test that UnsupportedUnitError is handled as ConversionError."""
        response = test_client.get("/test-unsupported-unit")

        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "ConversionError"
        assert "parsec" in data["detail"]
        assert data["type"] == "UnsupportedUnitError"

    def test_dimensionality_error_handled(self, test_client):
        """Test that DimensionalityConversionError is handled."""
        response = test_client.get("/test-dimensionality-error")

        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "ConversionError"
        assert "meter" in data["detail"]
        assert "second" in data["detail"]
        assert data["type"] == "DimensionalityConversionError"

    def test_negative_value_error_handled(self, test_client):
        """Test that NegativeValueError is handled."""
        response = test_client.get("/test-negative-value-error")

        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "ConversionError"
        assert "weight" in data["detail"]
        assert data["type"] == "NegativeValueError"


@pytest.mark.integration
class TestValidationErrorHandler:
    """Test Pydantic ValidationError handler."""

    @pytest.fixture
    def test_app(self):
        """Create test app with error handlers."""
        from pydantic import BaseModel, Field

        app = FastAPI()
        register_exception_handlers(app)

        class TestModel(BaseModel):
            value: int = Field(..., gt=0)
            name: str

        @app.post("/test-validation")
        async def test_endpoint(data: TestModel):
            return {"success": True}

        return app

    @pytest.fixture
    def test_client(self, test_app):
        """Create test client."""
        return TestClient(test_app)

    def test_validation_error_returns_422(self, test_client):
        """Test that validation errors return 422 status code."""
        response = test_client.post(
            "/test-validation",
            json={"value": "not_a_number", "name": "test"}
        )

        assert response.status_code == 422

    def test_validation_error_response_format(self, test_client):
        """Test ValidationError response format."""
        response = test_client.post(
            "/test-validation",
            json={"value": "invalid"}  # Missing name, invalid value
        )

        assert response.status_code == 422
        data = response.json()
        # FastAPI returns detail list by default
        assert "detail" in data
        assert isinstance(data["detail"], list)

    def test_validation_error_includes_field_info(self, test_client):
        """Test that validation errors include field information."""
        response = test_client.post(
            "/test-validation",
            json={"value": -1, "name": "test"}  # Invalid: value must be > 0
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        errors = data["detail"]
        assert len(errors) > 0

        # Check error structure
        error = errors[0]
        assert "loc" in error
        assert "msg" in error
        assert "type" in error

    def test_validation_error_missing_required_field(self, test_client):
        """Test validation error for missing required field."""
        response = test_client.post(
            "/test-validation",
            json={"value": 10}  # Missing name
        )

        assert response.status_code == 422
        data = response.json()
        errors = data["detail"]
        # Should have error for missing name field
        assert any("name" in str(error["loc"]) for error in errors)


@pytest.mark.integration
class TestGenericExceptionHandler:
    """Test generic Exception handler."""

    @pytest.fixture
    def test_app(self):
        """Create test app with error handlers."""
        app = FastAPI()
        register_exception_handlers(app)

        @app.get("/test-generic-error")
        async def trigger_generic_error():
            raise ValueError("Unexpected error")

        @app.get("/test-runtime-error")
        async def trigger_runtime_error():
            raise RuntimeError("Runtime error")

        return app

    @pytest.fixture
    def test_client(self, test_app):
        """Create test client."""
        return TestClient(test_app, raise_server_exceptions=False)

    def test_generic_error_returns_500(self, test_client):
        """Test that generic exceptions return 500 status code."""
        response = test_client.get("/test-generic-error")

        assert response.status_code == 500

    def test_generic_error_response_format(self, test_client):
        """Test generic error response format."""
        response = test_client.get("/test-generic-error")

        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert "detail" in data
        assert data["error"] == "InternalServerError"
        # Generic message, not exposing internal error details
        assert "unexpected error" in data["detail"].lower()

    def test_generic_error_hides_internal_details(self, test_client):
        """Test that generic handler doesn't expose internal error details."""
        response = test_client.get("/test-generic-error")

        data = response.json()
        # Should not contain the actual error message "Unexpected error"
        assert "Unexpected error" not in data["detail"]
        # Should return safe, generic message
        assert "Please try again later" in data["detail"]

    def test_runtime_error_handled(self, test_client):
        """Test that RuntimeError is handled by generic handler."""
        response = test_client.get("/test-runtime-error")

        assert response.status_code == 500
        data = response.json()
        assert data["error"] == "InternalServerError"


@pytest.mark.integration
class TestErrorHandlerIntegration:
    """Test error handlers integration with actual API endpoints."""

    def test_actual_conversion_error_from_api(self, client):
        """Test that actual API conversion errors are handled correctly."""
        # Try to convert incompatible units
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "m2",  # Incompatible: linear to area
                "decimals": 2
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert data["error"] == "ConversionError"
        assert "type" in data

    def test_actual_validation_error_from_api(self, client):
        """Test that actual API validation errors are handled correctly."""
        # Send invalid data type
        response = client.post(
            "/length/convert",
            json={
                "value": "not_a_number",
                "from_unit": "m",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code == 422
        data = response.json()
        # FastAPI returns detail for validation errors
        assert "detail" in data
