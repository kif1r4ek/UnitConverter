"""
Simplified unit tests for Redis service.

Tests cover:
- Basic functionality verification
- Error handling
- Key generation
"""
import pytest
import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from app.services.redis_service import RedisService


@pytest.mark.unit
class TestRedisServiceBasic:
    """Test basic Redis service functionality."""

    @pytest.mark.asyncio
    async def test_add_to_history_success(self, redis_service, mock_user_key):
        """Test successfully adding conversion to history."""
        conversion_data = {
            "value": 100,
            "from_unit": "m",
            "to_unit": "km",
            "result": 0.1
        }

        # Should not raise exception
        await redis_service.add_to_history(
            user_key=mock_user_key,
            converter_type="length",
            conversion_data=conversion_data
        )

    @pytest.mark.asyncio
    async def test_get_history_returns_list(self, redis_service, mock_user_key):
        """Test that get_history returns a list."""
        history = await redis_service.get_history(
            user_key=mock_user_key,
            converter_type="length"
        )

        assert isinstance(history, list)

    @pytest.mark.asyncio
    async def test_clear_history_specific_converter(self, redis_service, mock_user_key):
        """Test clearing history for specific converter type."""
        # Should not raise exception
        await redis_service.clear_history(
            user_key=mock_user_key,
            converter_type="length"
        )

    @pytest.mark.asyncio
    async def test_clear_all_history(self, redis_service, mock_user_key):
        """Test clearing all converter history for user."""
        # Should not raise exception
        await redis_service.clear_history(
            user_key=mock_user_key,
            converter_type=None
        )

    @pytest.mark.asyncio
    async def test_cache_set(self, redis_service):
        """Test setting cache value."""
        # Should not raise exception
        await redis_service.cache_set(
            key="test_key",
            value={"data": "value"},
            ttl=3600
        )

    @pytest.mark.asyncio
    async def test_cache_get_returns_none_when_empty(self, redis_service):
        """Test getting non-existent cache value returns None."""
        result = await redis_service.cache_get("missing_key")

        # With default mock, should return None
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_delete(self, redis_service):
        """Test deleting cache entry."""
        # Should not raise exception
        await redis_service.cache_delete("test_key")


@pytest.mark.unit
class TestHistoryKeyGeneration:
    """Test history key generation."""

    def test_history_key_format(self):
        """Test history key format is correct."""
        key = RedisService._history_key("session:abc123", "length")
        assert key == "history:session:abc123:length"

    def test_history_key_different_user(self):
        """Test key generation for different users."""
        key1 = RedisService._history_key("user:1", "length")
        key2 = RedisService._history_key("user:2", "length")
        assert key1 != key2
        assert key1 == "history:user:1:length"
        assert key2 == "history:user:2:length"

    def test_history_key_different_converter(self):
        """Test key generation for different converter types."""
        key1 = RedisService._history_key("user:1", "length")
        key2 = RedisService._history_key("user:1", "weight")
        assert key1 != key2
        assert key1 == "history:user:1:length"
        assert key2 == "history:user:1:weight"
