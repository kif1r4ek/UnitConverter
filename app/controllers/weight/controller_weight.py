from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

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