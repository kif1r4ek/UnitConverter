"""
Global exception handlers for FastAPI application.

This module should be saved as: app/core/error_handlers.py

Usage in main.py:
    from app.core.error_handlers import register_exception_handlers

    app = FastAPI()
    register_exception_handlers(app)
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.exceptions import (
    ConversionError,
    UnsupportedUnitError,
    InvalidValueError,
    DimensionalityConversionError,
    NegativeValueError,
)


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI application.

    Usage in main.py:
        app = FastAPI()
        register_exception_handlers(app)
    """

    @app.exception_handler(ConversionError)
    async def conversion_error_handler(request: Request, exc: ConversionError):
        """Handle all conversion-related errors with 400 Bad Request"""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "ConversionError",
                "detail": str(exc),
                "type": exc.__class__.__name__
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors"""
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"]
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "detail": "Input validation failed",
                "errors": errors
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "An unexpected error occurred. Please try again later.",
            }
        )