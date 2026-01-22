from fastapi import APIRouter, Request, Depends, Header
from redis.asyncio import Redis

from app.core.config import settings
from app.core.redis import get_redis
from app.dependencies.common import templates, logger, get_user_key
from app.domain.exceptions import ConversionError
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.weight import SWeightConvertRequest
from app.services import convert_weight
from app.services.redis_service import RedisService

router = APIRouter(
    prefix="/weight",
    tags=["weight"],
)


@router.get("")
async def get_weight_page(request: Request):
    logger.debug(
        "weight_page_requested",
        client=request.client.host
    )

    response = templates.TemplateResponse(
        "weight.html",
        {"request": request, "title": "Конвертер веса"},
    )

    if not request.cookies.get("session_id"):
        import uuid
        response.set_cookie(
            key="session_id",
            value=str(uuid.uuid4()),
            max_age=settings.HISTORY_TTL * 30,  # 30 дней
            httponly=True,
            samesite="lax"
        )

    return response


@router.post("/convert", response_model=ConversionResponse)
async def convert(
        request: Request,
        payload: SWeightConvertRequest,
        redis: Redis = Depends(get_redis),
        user_agent: str | None = Header(None)
) -> ConversionResponse:
    """
    Convert weight from one unit to another.
    """

    logger.info(
        "conversion_requested",
        converter_type="weight",
        value=payload.value,
        from_unit=payload.from_unit,
        to_unit=payload.to_unit
    )

    try:
        result = convert_weight(
            value=payload.value,
            from_unit=payload.from_unit,
            to_unit=payload.to_unit
        )

        user_key = get_user_key(request)

        redis_service = RedisService(redis)
        await redis_service.add_to_history(
            user_key=user_key,
            converter_type="weight",
            conversion_data={
                "value": payload.value,
                "from_unit": str(payload.from_unit),
                "to_unit": str(payload.to_unit),
                "result": result,
                "user_agent": user_agent,
            }
        )

        logger.info(
            "conversion_success",
            converter_type="weight",
            value=payload.value,
            from_unit=payload.from_unit,
            to_unit=payload.to_unit,
            result=result
        )

        return ConversionResponse(
            result=result,
            original_value=payload.value,
            from_unit=payload.from_unit,
            to_unit=payload.to_unit
        )

    except Exception as e:
        logger.error(
            "conversion_failed",
            converter_type="weight",
            value=payload.value,
            from_unit=payload.from_unit,
            to_unit=payload.to_unit,
            error=str(e),
            exc_info=True
        )
        raise ConversionError(str(e))


@router.get("/history")
async def get_history(
        request: Request,
        redis: Redis = Depends(get_redis)
):
    """Get conversion history from Redis."""

    user_key = get_user_key(request)
    redis_service = RedisService(redis)

    history = await redis_service.get_history(
        user_key=user_key,
        converter_type="weight"
    )

    return {"history": history}


@router.delete("/history")
async def clear_history(
        request: Request,
        redis: Redis = Depends(get_redis)
):
    """Clear conversion history."""

    user_key = get_user_key(request)
    redis_service = RedisService(redis)

    await redis_service.clear_history(
        user_key=user_key,
        converter_type="weight"
    )

    return {"message": "History cleared"}
