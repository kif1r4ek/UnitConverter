from fastapi import APIRouter, Request
from app.dependencies.common import templates
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.temperature import STemperatureConvertRequest
from app.services import convert_temperature

router = APIRouter(
    prefix="/temperature",
    tags=["temperature"],
)

@router.get("")
async def get_temperature_page(request: Request):
    return templates.TemplateResponse(
        "temperature.html",
        {"request": request, "title": "Конвертер температуры"},
    )


@router.post("/convert", response_model=ConversionResponse)
async def convert(request: STemperatureConvertRequest) -> ConversionResponse:
    """
    Convert temperature from one unit to another

    Args:
        request: Validated conversion request

    Returns:
        ConversionResponse with result
    """
    result = convert_temperature(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    return ConversionResponse(
        result=result,
        original_value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit)