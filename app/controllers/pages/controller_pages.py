from fastapi import APIRouter, Request
from app.dependencies.common import templates

router = APIRouter(
    tags=["pages"]
)

@router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
