from fastapi import APIRouter, Request
from app.dependencies.common import templates
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.weight import SWeightConvertRequest
from app.services import convert_weight

router = APIRouter(
    prefix="/weight",
    tags=["weight"],
)

@router.get("")
async def get_weight_page(request: Request):
    return templates.TemplateResponse(
        "weight.html",
        {"request": request, "title": "Конвертер веса"}
    )


@router.post("/convert", response_model=ConversionResponse)
async def convert(request: SWeightConvertRequest) -> ConversionResponse:
    """
    Convert weight from one unit to another

    Args:
        request: Validated conversion request

    Returns:
        ConversionResponse with result
    """
    result = convert_weight(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    return ConversionResponse(
        result=result,
        original_value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit)
