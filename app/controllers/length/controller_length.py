from fastapi import APIRouter, Request
from app.dependencies.common import templates

router = APIRouter(
    prefix="/length",
    tags=["length"],
)

@router.get("")
async def get_length_page(request: Request):
    return templates.TemplateResponse(
        "length.html",
        {"request": request},
    )
