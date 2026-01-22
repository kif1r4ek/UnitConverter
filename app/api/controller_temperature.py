from fastapi import APIRouter, Request, Depends, Header
from redis.asyncio import Redis

from app.core.config import settings
from app.core.redis import get_redis
from app.dependencies.common import templates, logger, get_user_key
from app.domain.exceptions import ConversionError
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.temperature import STemperatureConvertRequest
from app.services import convert_temperature
from app.services.redis_service import RedisService

router = APIRouter(
    prefix="/temperature",
    tags=["temperature"],
)


@router.get("")
async def get_temperature_page(request: Request):
    logger.debug(
        "temperature_page_requested",
        client=request.client.host
    )

    response = templates.TemplateResponse(
        "temperature.html",
        {"request": request, "title": "Конвертер температуры"},
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
        payload: STemperatureConvertRequest,
        redis: Redis = Depends(get_redis),
        user_agent: str | None = Header(None)
) -> ConversionResponse:
    """
    Convert temperature from one unit to another.
    """

    logger.info(
        "conversion_requested",
        converter_type="temperature",
        value=payload.value,
        from_unit=payload.from_unit,
        to_unit=payload.to_unit
    )

    try:
        result = convert_temperature(
            value=payload.value,
            from_unit=payload.from_unit,
            to_unit=payload.to_unit
        )

        user_key = get_user_key(request)

        redis_service = RedisService(redis)
        await redis_service.add_to_history(
            user_key=user_key,
            converter_type="temperature",
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
            converter_type="temperature",
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
            converter_type="temperature",
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
        converter_type="temperature"
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
        converter_type="temperature"
    )

    return {"message": "History cleared"}
