from fastapi import HTTPException, status

from typing import Optional


class ConversionError(Exception):
    """
    Base exception for all conversion-related errors.

    Attributes:
        message: Human-readable error message
        from_unit: Source unit (optional)
        to_unit: Target unit (optional)
        value: Original value (optional)
    """

    def __init__(
        self,
        message: str,
        *,
        from_unit: Optional[str] = None,
        to_unit: Optional[str] = None,
        value: Optional[float] = None,
    ) -> None:
        self.message = message
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.value = value
        super().__init__(message)

    def __str__(self) -> str:
        details = [self.message]

        if self.value is not None:
            details.append(f"value={self.value}")
        if self.from_unit:
            details.append(f"from={self.from_unit}")
        if self.to_unit:
            details.append(f"to={self.to_unit}")

        return " | ".join(details)


class UnsupportedUnitError(ConversionError):
    """
    Raised when a unit is not supported by the converter.
    """

    def __init__(
        self,
        unit: str,
        *,
        from_unit: Optional[str] = None,
        to_unit: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=f"Unsupported unit: {unit}",
            from_unit=from_unit,
            to_unit=to_unit,
        )
        self.unit = unit


class InvalidValueError(ConversionError):
    """
    Raised when the provided value is invalid for conversion.
    """

    def __init__(self, value: float, reason: Optional[str] = None) -> None:
        message = "Invalid value"
        if reason:
            message += f": {reason}"

        super().__init__(
            message=message,
            value=value,
        )
        self.reason = reason

def http_400(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def http_500(detail: str = "Internal server error") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )