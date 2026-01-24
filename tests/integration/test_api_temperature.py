"""
Integration tests for temperature conversion API endpoints.

Tests cover:
- POST /temperature/convert endpoint
- GET /temperature/history endpoint
- DELETE /temperature/history endpoint
- Negative temperature handling
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestTemperatureConvertEndpoint:
    """Test POST /temperature/convert endpoint."""

    def test_convert_celsius_to_fahrenheit_freezing(self, client):
        """Test freezing point conversion (0°C to °F)."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 0,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 32.0
        assert data["original_value"] == 0
        assert data["from_unit"] == "celsius"
        assert data["to_unit"] == "fahrenheit"

    def test_convert_celsius_to_fahrenheit_boiling(self, client):
        """Test boiling point conversion (100°C to °F)."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 100,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 212.0

    def test_convert_fahrenheit_to_celsius(self, client):
        """Test °F to °C conversion."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 32,
                "from_unit": "fahrenheit",
                "to_unit": "celsius",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_convert_celsius_to_kelvin(self, client):
        """Test °C to K conversion."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 0,
                "from_unit": "celsius",
                "to_unit": "kelvin",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 273.15

    def test_convert_kelvin_to_celsius(self, client):
        """Test K to °C conversion."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 273.15,
                "from_unit": "kelvin",
                "to_unit": "celsius",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_convert_negative_celsius_allowed(self, client):
        """Test that negative Celsius temperatures are allowed."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": -40,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -40.0

    def test_convert_negative_fahrenheit_allowed(self, client):
        """Test that negative Fahrenheit temperatures are allowed."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": -40,
                "from_unit": "fahrenheit",
                "to_unit": "celsius",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -40.0

    def test_convert_absolute_zero(self, client):
        """Test absolute zero conversion (0K to °C)."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 0,
                "from_unit": "kelvin",
                "to_unit": "celsius",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == -273.15

    def test_convert_body_temperature(self, client):
        """Test body temperature conversion (37°C to °F)."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 37,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 98.6

    def test_convert_invalid_unit(self, client):
        """Test that invalid temperature units are rejected."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 100,
                "from_unit": "invalid",
                "to_unit": "celsius",
                "decimals": 2
            }
        )

        assert response.status_code == 422

    def test_convert_missing_value(self, client):
        """Test that missing value is rejected."""
        response = client.post(
            "/temperature/convert",
            json={
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 2
            }
        )

        assert response.status_code == 422

    def test_convert_custom_decimals(self, client):
        """Test conversion with custom decimal places."""
        response = client.post(
            "/temperature/convert",
            json={
                "value": 25,
                "from_unit": "celsius",
                "to_unit": "fahrenheit",
                "decimals": 4
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 77.0


@pytest.mark.integration
@pytest.mark.redis
class TestTemperatureHistoryEndpoints:
    """Test temperature history endpoints."""

    def test_get_temperature_history(self, client):
        """Test retrieving temperature conversion history."""
        response = client.get("/temperature/history")

        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)

    def test_clear_temperature_history(self, client):
        """Test clearing temperature conversion history."""
        response = client.delete("/temperature/history")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data


@pytest.mark.integration
class TestTemperaturePageEndpoint:
    """Test temperature page rendering."""

    def test_get_temperature_page(self, client):
        """Test rendering temperature conversion page."""
        response = client.get("/temperature")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
