import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = structlog.get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)
        start_time = time.time()

        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client=request.client.host,
        )

        try:
            response = await call_next(request)

            duration = time.time() - start_time
            logger.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            return response
        except Exception as e:
            duration = time.time() - start_time

            logger.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
                duration=duration,
                exc_info=True
            )
            raise
        finally:
            structlog.contextvars.clear_contextvars()