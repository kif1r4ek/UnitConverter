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

configure_logger()
logger = get_logger(__name__)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(pages)
app.include_router(length)
app.include_router(temperature)
app.include_router(weight)

@app.on_event("startup")
async def startup_event():
    logger.info(
        "application_started",
        app_name=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        debug=settings.DEBUG,
    )

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_shutdown")

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host=settings.HOST, port=settings.PORT)