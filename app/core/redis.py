"""
Redis connection manager.

Manages Redis connection pool lifecycle and provides
async context manager for safe connection handling.
"""

from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings
from app.dependencies.common import logger

class RedisManager:
    """
    Redis connection pool manager.

    Uses connection pooling for efficient resource usage.
    Implements singleton pattern to ensure single pool instance.

    Example:
        redis_manager = RedisManager()
        await redis_manager.connect()

        async with redis_manager.get_client() as redis:
            await redis.set('key', 'value')

        await redis_manager.disconnect()
    """

    def __init__(self):
        self._redis: Redis | None = None

    async def connect(self) -> None:
        self._redis = Redis.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            socket_keepalive=True,
            socket_connect_timeout=5,
            retry_on_timeout=True,
        )

        await self._redis.ping()

        logger.info(
            "redis_connected",
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
        )

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.aclose()
            logger.info("redis_disconnected")

    def get_client(self) -> Redis:
        if not self._redis:
            raise RuntimeError("Redis not initialized")
        return self._redis

    async def health_check(self) -> bool:
        try:
            await self.get_client().ping()
            return True
        except Exception as e:
            logger.error("redis_health_check_failed", error=str(e))
            return False


redis_manager = RedisManager()


def get_redis() -> Redis:
    """
    Dependency injection для FastAPI.

    Usage in router:
        @router.get("/")
        async def endpoint(redis: Redis = Depends(get_redis)):
            await redis.set('key', 'value')
    """
    return redis_manager.get_client()



