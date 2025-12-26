from fastapi import APIRouter, Request
from app.dependencies.common import templates

router = APIRouter(
    prefix="/temperature",
    tags=["temperature"],
)

@router.get("")
async def get_temperature_page(request: Request):
    return templates.TemplateResponse(
        "temperature.html",
        {"request": request},
    )
