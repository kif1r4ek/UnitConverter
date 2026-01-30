"""
Integration tests for health check and main page endpoints.

Tests cover:
- GET / (home page)
- GET /health (health check with Redis status)
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestHomePageEndpoint:
    """Test GET / home page endpoint."""

    def test_get_home_page_success(self, client):
        """Test rendering home page."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")


@pytest.mark.integration
@pytest.mark.redis
class TestHealthCheckEndpoint:
    """Test GET /health health check endpoint."""

    @patch('app.main.redis_manager.health_check')
    def test_health_check_redis_healthy(self, mock_health_check, client):
        """Test health check when Redis is healthy."""
        mock_health_check.return_value = True

        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "redis" in data
        assert data["redis"] is True

    @patch('app.main.redis_manager.health_check')
    def test_health_check_redis_unhealthy(self, mock_health_check, client):
        """Test health check when Redis is unhealthy."""
        mock_health_check.return_value = False

        response = client.get("/health")

        # Application should still return 200 but indicate Redis issue
        assert response.status_code == 200
        data = response.json()
        assert "redis" in data
        assert data["redis"] is False
