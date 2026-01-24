"""
High-level Redis operations for the application.

Provides abstraction layer over raw Redis commands
with domain-specific methods.
"""
import json
from datetime import datetime
from typing import Any
from datetime import datetime, timezone
from redis.asyncio import Redis
from app.utils.time import format_relative_time
from app.core.config import settings
from app.dependencies.common import logger


class RedisService:
    """
    Service layer for Redis operations.

    Provides high-level methods for common operations:
    - History management
    - Caching
    - Session management
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def add_to_history(
            self,
            user_key: str,
            converter_type: str,
            conversion_data: dict[str, Any]
    ) -> None:
        """
        Add conversion to user's history.

        Args:
            user_key: Unique user identifier (session_id, user_id, IP)
            converter_type: Type of converter (length, weight, temperature)
            conversion_data: Conversion details (value, from_unit, to_unit, result)

        Example:
            await service.add_to_history(
                user_key="session:abc123",
                converter_type="length",
                conversion_data={
                    "value": 100,
                    "from_unit": "m",
                    "to_unit": "km",
                    "result": 0.1,
                    "timestamp": "2024-01-16T12:00:00"
                }
            )
        """
        conversion_data["created_at"] = datetime.now(timezone.utc).isoformat()

        key = self._history_key(user_key, converter_type)

        try:
            if "timestamp" not in conversion_data:
                conversion_data["timestamp"] = datetime.utcnow().isoformat()

            item = json.dumps(conversion_data)

            await self.redis.lpush(key, item)

            await self.redis.ltrim(key, 0, settings.MAX_HISTORY_ITEMS - 1)

            await self.redis.expire(key, settings.HISTORY_TTL)

            logger.debug(
                "history_item_added",
                user_key=user_key,
                converter_type=converter_type
            )

        except Exception as e:
            logger.error(
                "failed_to_add_history",
                user_key=user_key,
                error=str(e),
                exc_info=True
            )

    async def get_history(
            self,
            user_key: str,
            converter_type: str,
            limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get user's conversion history with human-readable timestamps.
        """
        key = self._history_key(user_key, converter_type)

        try:
            limit = limit or settings.MAX_HISTORY_ITEMS
            items = await self.redis.lrange(key, 0, limit - 1)
            history = []

            for item in items:
                data = json.loads(item)

                # Если нет created_at, добавляем текущее время
                if "created_at" not in data:
                    data["created_at"] = datetime.now(timezone.utc).isoformat()

                # Генерируем поле created_at_human
                data["created_at_human"] = format_relative_time(data["created_at"])

                history.append(data)

            logger.debug(
                "history_retrieved",
                user_key=user_key,
                converter_type=converter_type,
                count=len(history)
            )

            return history

        except Exception as e:
            logger.error(
                "failed_to_get_history",
                user_key=user_key,
                error=str(e),
                exc_info=True
            )
            return []

    async def clear_history(
            self,
            user_key: str,
            converter_type: str | None = None
    ) -> None:
        """
        Clear user's history.

        Args:
            user_key: Unique user identifier
            converter_type: Specific converter or None for all
        """

        try:
            if converter_type:
                key = self._history_key(user_key, converter_type)
                await self.redis.delete(key)
            else:
                pattern = f"history:{user_key}:*"
                keys = await self.redis.keys(pattern)
                if keys:
                    await self.redis.delete(*keys)

            logger.info(
                "history_cleared",
                user_key=user_key,
                converter_type=converter_type
            )

        except Exception as e:
            logger.error(
                "failed_to_clear_history",
                user_key=user_key,
                error=str(e),
                exc_info=True
            )

    async def cache_set(
            self,
            key: str,
            value: Any,
            ttl: int = 3600
    ) -> None:
        """
        Set cache value with TTL.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (default: 1 hour)
        """
        try:
            serialized  = json.dumps(value)
            await self.redis.setex(key, ttl, serialized)

            logger.debug("cache_set", key=key, ttl=ttl)
        except Exception as e:
            logger.error("cache_set_failed", key=key, error=str(e))

    async def cache_get(self, key: str) -> Any | None:
        """
        Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """

        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("cache_get_failed", key=key, error=str(e))
            return None

    async def cache_delete(self, key: str) -> None:
        """Delete cache entry."""
        try:
            await self.redis.delete(key)
            logger.debug("cache_deleted", key=key)
        except Exception as e:
            logger.error("cache_delete_failed", key=key, error=str(e))

    @staticmethod
    def _history_key(user_key: str, converter_type: str) -> str:
        """
        Generate Redis key for history.

        Pattern: history:{user_key}:{converter_type}
        Example: history:session:abc123:length
        """
        return f"history:{user_key}:{converter_type}"