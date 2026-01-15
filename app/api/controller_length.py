from fastapi import APIRouter, Request

from app.core.logger import get_logger
from app.dependencies.common import templates
from app.domain.exceptions import ConversionError
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.length import SLengthConvertRequest
from app.services import convert_length



logger = get_logger(__name__)
router = APIRouter(
    prefix="/length",
    tags=["length"],
)

@router.get("")
async def get_length_page(request: Request):
    logger.debug("length_page_requested", client=request.client.host)
    return templates.TemplateResponse(
        "length.html",
        {"request": request, "title": "Конвертер длины"},
    )

@router.post("/convert", response_model=ConversionResponse)
async def convert(request: SLengthConvertRequest) -> ConversionResponse:
    """
    Convert length/area from one unit to another

    Args:
        request: Validated conversion request

    Returns:
        ConversionResponse with result
    """
    logger.info(
        "conversion_requested",
        converter_type="length",
        value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit
    )

    try:
        result = convert_length(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)

        logger.info(
            "conversion_success",
            converter_type="length",
            value=request.value,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            result=result
        )

        return ConversionResponse(
            result=result,
            original_value=request.value,
            from_unit=request.from_unit,
            to_unit=request.to_unit)

    except Exception as e:
        logger.error(
            "conversion_failed",
            converter_type="length",
            value=request.value,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            error=str(e),
            exc_info=True
        )

        raise ConversionError(str(e))
