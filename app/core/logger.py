import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog

from app.core.config import settings


def configure_logger() -> None:
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = logging._nameToLevel[settings.LOG_LEVEL]

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.handlers.clear()

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
    ]

    json_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=shared_processors,
    )

    console_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(),
        foreign_pre_chain=shared_processors,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    app_file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(json_formatter)

    error_file_handler = RotatingFileHandler(
        settings.LOG_ERROR_FILE,
        maxBytes=settings.LOG_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(json_formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(error_file_handler)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None):
    return structlog.get_logger(name)
