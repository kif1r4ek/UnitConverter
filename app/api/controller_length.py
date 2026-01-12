from fastapi import APIRouter, Request
from app.dependencies.common import templates
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.length import SLengthConvertRequest
from app.services import convert_length

router = APIRouter(
    prefix="/length",
    tags=["length"],
)

@router.get("")
async def get_length_page(request: Request):
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
    result = convert_length(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    return ConversionResponse(
        result=result,
        original_value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit)
