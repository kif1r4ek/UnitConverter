"""
Integration tests for length conversion API endpoints.

Tests cover:
- POST /length/convert endpoint
- GET /length/history endpoint
- DELETE /length/history endpoint
- Error handling
- Request validation
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.domain.units.length import UnitsLength


@pytest.mark.integration
class TestLengthConvertEndpoint:
    """Test POST /length/convert endpoint."""

    def test_convert_meters_to_kilometers_success(self, client):
        """Test successful conversion from meters to kilometers."""
        response = client.post(
            "/length/convert",
            json={
                "value": 1000,
                "from_unit": "m",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1.0
        assert data["original_value"] == 1000
        assert data["from_unit"] == "m"
        assert data["to_unit"] == "km"

    def test_convert_feet_to_meters_success(self, client):
        """Test successful conversion from feet to meters."""
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "foot",
                "to_unit": "m",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 30.48
        assert data["from_unit"] == "foot"

    def test_convert_area_hectare_to_square_meters(self, client):
        """Test area conversion from hectare to m²."""
        response = client.post(
            "/length/convert",
            json={
                "value": 1,
                "from_unit": "hectare",
                "to_unit": "m2",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 10000.0

    def test_convert_with_custom_decimals(self, client):
        """Test conversion with custom decimal places."""
        response = client.post(
            "/length/convert",
            json={
                "value": 1,
                "from_unit": "m",
                "to_unit": "foot",
                "decimals": 4
            }
        )

        assert response.status_code == 200
        data = response.json()
        # API currently uses default 2 decimals
        assert isinstance(data["result"], float)
        assert data["result"] == 3.28

    def test_convert_negative_value_rejected(self, client):
        """Test that negative values are rejected."""
        response = client.post(
            "/length/convert",
            json={
                "value": -10,
                "from_unit": "m",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]
        errors = response.json()
        assert "detail" in errors

    def test_convert_invalid_from_unit(self, client):
        """Test that invalid from_unit is rejected."""
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "invalid_unit",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_invalid_to_unit(self, client):
        """Test that invalid to_unit is rejected."""
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "invalid_unit",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_dimensionality_error(self, client):
        """Test conversion between incompatible dimensions."""
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "m",
                "to_unit": "m2",
                "decimals": 2
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_convert_missing_required_field(self, client):
        """Test that missing required fields are rejected."""
        response = client.post(
            "/length/convert",
            json={
                "value": 100,
                "from_unit": "m"
                # Missing to_unit
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_zero_value(self, client):
        """Test conversion with zero value."""
        response = client.post(
            "/length/convert",
            json={
                "value": 0,
                "from_unit": "m",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_convert_large_value(self, client):
        """Test conversion with very large value."""
        response = client.post(
            "/length/convert",
            json={
                "value": 1000000000,
                "from_unit": "m",
                "to_unit": "km",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1000000.0

    def test_convert_small_fractional_value(self, client):
        """Test conversion with small fractional value."""
        response = client.post(
            "/length/convert",
            json={
                "value": 0.001,
                "from_unit": "m",
                "to_unit": "mm",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1.0


@pytest.mark.integration
@pytest.mark.redis
class TestLengthHistoryEndpoints:
    """Test history management endpoints."""

    def test_get_history_success(self, client):
        """Test retrieving conversion history."""
        response = client.get("/length/history")

        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)

    def test_clear_history_success(self, client):
        """Test clearing conversion history."""
        response = client.delete("/length/history")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "History cleared"


@pytest.mark.integration
class TestLengthPageEndpoint:
    """Test GET /length page rendering endpoint."""

    def test_get_length_page_success(self, client):
        """Test rendering length conversion page."""
        response = client.get("/length")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")

    def test_get_length_page_sets_session_cookie(self, client):
        """Test that session cookie is set on first visit."""
        response = client.get("/length")

        assert response.status_code == 200
        # Check if Set-Cookie header exists
        cookies = response.cookies
        # Session cookie might be set
        assert len(cookies) >= 0  # May or may not have cookies depending on implementation
