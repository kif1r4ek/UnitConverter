"""
Integration tests for weight conversion API endpoints.

Tests cover:
- POST /weight/convert endpoint
- GET /weight/history endpoint
- DELETE /weight/history endpoint
- Validation and error handling
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestWeightConvertEndpoint:
    """Test POST /weight/convert endpoint."""

    def test_convert_kilograms_to_pounds(self, client):
        """Test kg to lb conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "kg",
                "to_unit": "lb",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 2.2
        assert data["original_value"] == 1
        assert data["from_unit"] == "kg"
        assert data["to_unit"] == "lb"

    def test_convert_pounds_to_kilograms(self, client):
        """Test lb to kg conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "lb",
                "to_unit": "kg",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.45

    def test_convert_grams_to_milligrams(self, client):
        """Test g to mg conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "g",
                "to_unit": "mg",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1000.0

    def test_convert_stone_to_pounds(self, client):
        """Test stone to pounds conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "stone",
                "to_unit": "lb",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 14.0

    def test_convert_ounces_to_grams(self, client):
        """Test oz to g conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "oz",
                "to_unit": "g",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 28.35

    def test_convert_tons_to_kilograms(self, client):
        """Test metric ton to kg conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "ton",
                "to_unit": "kg",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1000.0

    def test_convert_ton_us_to_kilograms(self, client):
        """Test US ton to kg conversion."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "ton_us",
                "to_unit": "kg",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 907.18

    def test_convert_negative_value_rejected(self, client):
        """Test that negative weight values are rejected."""
        response = client.post(
            "/weight/convert",
            json={
                "value": -10,
                "from_unit": "kg",
                "to_unit": "lb",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]
        errors = response.json()
        assert "detail" in errors

    def test_convert_zero_value(self, client):
        """Test conversion with zero value."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 0,
                "from_unit": "kg",
                "to_unit": "lb",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 0.0

    def test_convert_large_value(self, client):
        """Test conversion with large value."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1000000,
                "from_unit": "kg",
                "to_unit": "ton",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1000.0

    def test_convert_small_fractional_value(self, client):
        """Test conversion with small fractional value."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 0.001,
                "from_unit": "g",
                "to_unit": "mg",
                "decimals": 2
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1.0

    def test_convert_invalid_from_unit(self, client):
        """Test that invalid from_unit is rejected."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 100,
                "from_unit": "invalid",
                "to_unit": "kg",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_invalid_to_unit(self, client):
        """Test that invalid to_unit is rejected."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 100,
                "from_unit": "kg",
                "to_unit": "invalid",
                "decimals": 2
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_missing_required_field(self, client):
        """Test that missing required fields are rejected."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 100,
                "from_unit": "kg"
                # Missing to_unit
            }
        )

        assert response.status_code in [400, 422]

    def test_convert_with_custom_decimals(self, client):
        """Test conversion with custom decimal places."""
        response = client.post(
            "/weight/convert",
            json={
                "value": 1,
                "from_unit": "kg",
                "to_unit": "lb",
                "decimals": 4
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 2.2


@pytest.mark.integration
@pytest.mark.redis
class TestWeightHistoryEndpoints:
    """Test weight history endpoints."""

    def test_get_weight_history(self, client):
        """Test retrieving weight conversion history."""
        response = client.get("/weight/history")

        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)

    def test_clear_weight_history(self, client):
        """Test clearing weight conversion history."""
        response = client.delete("/weight/history")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data


@pytest.mark.integration
class TestWeightPageEndpoint:
    """Test weight page rendering."""

    def test_get_weight_page(self, client):
        """Test rendering weight conversion page."""
        response = client.get("/weight")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
