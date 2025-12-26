from fastapi import APIRouter, Request
from app.dependencies.common import templates

router = APIRouter(
    prefix="/weight",
    tags=["weight"],
)

@router.get("")
async def get_weight_page(request: Request):
    return templates.TemplateResponse(
        "weight.html",
        {"request": request}
    )