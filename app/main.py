from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.api.controller_pages import router as pages
from app.api.controller_length import router as length
from app.api.controller_temperature import router as temperature
from app.api.controller_weight import router as weight
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.core.logger import configure_logger, get_logger
from app.core.middleware import LoggingMiddleware
from app.dependencies.common import logger
from app.core.redis import redis_manager

configure_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI application.

    Handles startup and shutdown events:
    - Connect to Redis on startup
    - Disconnect from Redis on shutdown
    """
    logger.info("application_startup_initiated")

    try:
        await redis_manager.connect()
        logger.info("redis_initialized")
    except Exception as e:
        logger.error("redis_initialization_failed", error=str(e))
        raise

    logger.info(
        "application_started",
        app_name=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        debug=settings.DEBUG,
    )

    yield

    logger.info("application_shutdown_initiated")
    await redis_manager.disconnect()
    logger.info("application_shutdown_complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(pages)
app.include_router(length)
app.include_router(temperature)
app.include_router(weight)

@app.get("/health", include_in_schema=False)
async def health():
    redis_ok = await redis_manager.health_check()
    return {
        "status": "ok",
        "redis": redis_ok,
    }

# if __name__ == "__main__":
#      uvicorn.run("app.main:app", reload=True, host=settings.HOST, port=settings.PORT)