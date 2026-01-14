import logging
from logging.handlers import RotatingFileHandler

import structlog
from pathlib import Path

from app.core.config import settings


def configure_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(message)s)",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=settings.LOG_SIZE,
                backupCount=settings.LOG_BACKUP_COUNT
            ),
            RotatingFileHandler(
                settings.LOG_ERROR_FILE,
                maxBytes=settings.LOG_SIZE,
                backupCount=settings.LOG_BACKUP_COUNT
            )
        ]
    )

    structlog.configure_logger(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.add_logger_name,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],

        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO
        ),

        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    if settings.DEBUG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.dev.ConsoleRenderer(),
            ]
        )

    return structlog.get_logger()


def get_logger(name: str = None):
    return structlog.get_logger(name)