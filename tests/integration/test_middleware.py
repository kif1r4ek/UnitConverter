"""
Integration tests for middleware.

Tests cover:
- LoggingMiddleware request/response logging
- Request ID generation
- Duration tracking
- Error handling in middleware
"""
import pytest
import structlog
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.middleware import LoggingMiddleware


@pytest.mark.integration
class TestLoggingMiddleware:
    """Test LoggingMiddleware functionality."""

    @pytest.fixture
    def test_app(self):
        """Create a test FastAPI app with LoggingMiddleware."""
        app = FastAPI()
        app.add_middleware(LoggingMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "success"}

        @app.get("/test-error")
        async def test_error_endpoint():
            raise ValueError("Test error")

        return app

    @pytest.fixture
    def test_client(self, test_app):
        """Create test client with middleware-enabled app."""
        return TestClient(test_app)

    def test_middleware_adds_request_id(self, test_client):
        """Test that middleware generates and binds request ID."""
        with patch('app.core.middleware.structlog.contextvars.bind_contextvars') as mock_bind:
            response = test_client.get("/test")

            assert response.status_code == 200
            # Verify request_id was bound
            mock_bind.assert_called_once()
            call_kwargs = mock_bind.call_args[1]
            assert "request_id" in call_kwargs
            # Request ID should be a UUID string
            assert len(call_kwargs["request_id"]) == 36  # UUID length

    def test_middleware_logs_request_started(self, test_client):
        """Test that middleware logs request start."""
        with patch('app.core.middleware.logger.info') as mock_log:
            response = test_client.get("/test")

            assert response.status_code == 200
            # Check that request_started was logged
            calls = [call for call in mock_log.call_args_list if call[0][0] == "request_started"]
            assert len(calls) > 0

            # Verify logged data
            first_call = calls[0]
            assert first_call[1]["method"] == "GET"
            assert first_call[1]["path"] == "/test"

    def test_middleware_logs_request_completed(self, test_client):
        """Test that middleware logs successful request completion."""
        with patch('app.core.middleware.logger.info') as mock_log:
            response = test_client.get("/test")

            assert response.status_code == 200
            # Check that request_completed was logged
            calls = [call for call in mock_log.call_args_list if call[0][0] == "request_completed"]
            assert len(calls) > 0

            # Verify logged data
            completed_call = calls[0]
            assert completed_call[1]["method"] == "GET"
            assert completed_call[1]["path"] == "/test"
            assert completed_call[1]["status_code"] == 200
            assert "duration" in completed_call[1]
            assert completed_call[1]["duration"] >= 0

    def test_middleware_logs_request_failed(self, test_client):
        """Test that middleware logs failed requests."""
        with patch('app.core.middleware.logger.error') as mock_error:
            # This will raise ValueError
            with pytest.raises(ValueError):
                test_client.get("/test-error")

            # Check that request_failed was logged
            calls = [call for call in mock_error.call_args_list if call[0][0] == "request_failed"]
            assert len(calls) > 0

            # Verify logged data
            error_call = calls[0]
            assert error_call[1]["method"] == "GET"
            assert error_call[1]["path"] == "/test-error"
            assert "error" in error_call[1]
            assert "duration" in error_call[1]
            assert error_call[1]["exc_info"] is True

    def test_middleware_clears_context_vars(self, test_client):
        """Test that middleware clears context variables after request."""
        with patch('app.core.middleware.structlog.contextvars.clear_contextvars') as mock_clear:
            response = test_client.get("/test")

            assert response.status_code == 200
            # Verify context was cleared
            mock_clear.assert_called()

    def test_middleware_clears_context_vars_on_error(self, test_client):
        """Test that context variables are cleared even on error."""
        with patch('app.core.middleware.structlog.contextvars.clear_contextvars') as mock_clear:
            with pytest.raises(ValueError):
                test_client.get("/test-error")

            # Verify context was cleared despite error
            mock_clear.assert_called()

    def test_middleware_tracks_duration(self, test_client):
        """Test that middleware accurately tracks request duration."""
        with patch('app.core.middleware.logger.info') as mock_log:
            response = test_client.get("/test")

            assert response.status_code == 200

            # Get the request_completed log
            completed_calls = [call for call in mock_log.call_args_list if call[0][0] == "request_completed"]
            assert len(completed_calls) > 0

            duration = completed_calls[0][1]["duration"]
            # Duration should be positive and reasonable (< 1 second for this simple endpoint)
            assert 0 <= duration < 1

    def test_middleware_logs_different_methods(self, test_app):
        """Test that middleware logs different HTTP methods correctly."""
        @test_app.post("/test-post")
        async def test_post():
            return {"message": "posted"}

        client = TestClient(test_app)

        with patch('app.core.middleware.logger.info') as mock_log:
            response = client.post("/test-post")

            assert response.status_code == 200

            started_calls = [call for call in mock_log.call_args_list if call[0][0] == "request_started"]
            assert any(call[1]["method"] == "POST" for call in started_calls)

    def test_middleware_logs_different_paths(self, test_client):
        """Test that middleware correctly logs different paths."""
        with patch('app.core.middleware.logger.info') as mock_log:
            test_client.get("/test")

            started_calls = [call for call in mock_log.call_args_list if call[0][0] == "request_started"]
            assert any(call[1]["path"] == "/test" for call in started_calls)
