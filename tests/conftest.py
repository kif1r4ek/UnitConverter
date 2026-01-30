"""
Pytest configuration and shared fixtures for the test suite.
"""
import asyncio
import pytest
from typing import AsyncGenerator, Generator, Any
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from starlette.testclient import TestClient

from app.main import app
from app.core.redis import RedisManager
from app.services.redis_service import RedisService


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_redis() -> AsyncMock:
    """
    Mock Redis client for testing without actual Redis connection.

    Returns:
        AsyncMock: Mocked Redis client with common methods
    """
    redis_mock = AsyncMock(spec=Redis)

    # Setup default behaviors for common operations
    redis_mock.ping = AsyncMock(return_value=True)
    redis_mock.lpush = AsyncMock(return_value=1)
    redis_mock.lrange = AsyncMock(return_value=[])
    redis_mock.ltrim = AsyncMock(return_value=True)
    redis_mock.expire = AsyncMock(return_value=True)
    redis_mock.delete = AsyncMock(return_value=1)
    redis_mock.keys = AsyncMock(return_value=[])
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.setex = AsyncMock(return_value=True)

    return redis_mock


@pytest.fixture
def redis_service(mock_redis: AsyncMock) -> RedisService:
    """
    Create RedisService instance with mocked Redis client.

    Args:
        mock_redis: Mocked Redis client

    Returns:
        RedisService: Service instance for testing
    """
    return RedisService(redis=mock_redis)


@pytest.fixture
async def mock_redis_manager(mock_redis: AsyncMock) -> AsyncGenerator[RedisManager, None]:
    """
    Mock RedisManager for integration tests.

    Yields:
        RedisManager: Mocked manager instance
    """
    manager = RedisManager()
    manager._redis = mock_redis
    manager._initialized = True

    yield manager

    # Cleanup
    manager._redis = None
    manager._initialized = False


@pytest.fixture
def client(mock_redis) -> Generator[TestClient, Any, None]:
    """
    Create FastAPI test client with mocked Redis.

    Returns:
        TestClient: Test client for making requests
    """
    # Override Redis dependency
    from app.core.redis import get_redis

    async def override_get_redis():
        return mock_redis

    app.dependency_overrides[get_redis] = override_get_redis

    client = TestClient(app)
    yield client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def mock_user_key() -> str:
    """
    Generate a mock user key for testing.

    Returns:
        str: Mock session-based user key
    """
    return "session:test-user-123"


@pytest.fixture
def sample_length_conversion() -> dict:
    """
    Sample length conversion data for testing.

    Returns:
        dict: Conversion data dictionary
    """
    return {
        "value": 100,
        "from_unit": "m",
        "to_unit": "km",
        "result": 0.1,
        "decimals": 2
    }


@pytest.fixture
def sample_temperature_conversion() -> dict:
    """
    Sample temperature conversion data for testing.

    Returns:
        dict: Conversion data dictionary
    """
    return {
        "value": 0,
        "from_unit": "celsius",
        "to_unit": "fahrenheit",
        "result": 32.0,
        "decimals": 2
    }


@pytest.fixture
def sample_weight_conversion() -> dict:
    """
    Sample weight conversion data for testing.

    Returns:
        dict: Conversion data dictionary
    """
    return {
        "value": 1,
        "from_unit": "kg",
        "to_unit": "lb",
        "result": 2.2,
        "decimals": 2
    }
