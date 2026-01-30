from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from app.core.config import settings
from app.core.logger import get_logger
from app.core.redis import get_redis
from app.dependencies.common import templates, logger, get_user_key, get_or_create_session
from app.domain.exceptions import ConversionError
from app.domain.models.forms import ConversionResponse
from app.domain.models.schemas.length import SLengthConvertRequest
from app.services import convert_length
from app.services.redis_service import RedisService

router = APIRouter(
    prefix="/length",
    tags=["length"],
)


@router.get("")
async def get_length_page(request: Request):
    logger.debug("length_page_requested", client=request.client.host)

    response = templates.TemplateResponse(
        "length.html",
        {"request": request, "title": "Конвертер длины"},
    )

    if not request.cookies.get("session_id"):
        import uuid
        response.set_cookie(
            key="session_id",
            value=str(uuid.uuid4()),
            max_age=settings.HISTORY_TTL,
            httponly=True,
            samesite="lax"
        )

    return response




@router.post("/convert", response_model=ConversionResponse)
async def convert(
        request: Request,
        pyload: SLengthConvertRequest,
        redis: Redis = Depends(get_redis),
        user_agent: str | None = Header(None)
) -> ConversionResponse:
    """
    Convert length/area from one unit to another

    Args:
        request: Validated conversion request

    Returns:
        ConversionResponse with result
        :param pyload:
        :param user_agent:
        :param request:
        :param redis:
    """
    logger.info(
        "conversion_requested",
        converter_type="length",
        value=pyload.value,
        from_unit=pyload.from_unit,
        to_unit=pyload.to_unit
    )

    try:
        result = convert_length(value=pyload.value, from_unit=pyload.from_unit, to_unit=pyload.to_unit)

        user_key, session_id, is_new = get_or_create_session(request)

        redis_service = RedisService(redis)
        await redis_service.add_to_history(
            user_key=user_key,
            converter_type="length",
            conversion_data={
                "value": pyload.value,
                "from_unit": str(pyload.from_unit),
                "to_unit": str(pyload.to_unit),
                "result": result,
                "user_agent": user_agent,
            }
        )

        logger.info(
            "conversion_success",
            converter_type="length",
            value=pyload.value,
            from_unit=pyload.from_unit,
            to_unit=pyload.to_unit,
            result=result
        )

        response_data = ConversionResponse(
            result=result,
            original_value=pyload.value,
            from_unit=pyload.from_unit,
            to_unit=pyload.to_unit
        )

        response = JSONResponse(content=response_data.dict())
        if is_new:
            response.set_cookie(
                key="session_id",
                value=session_id,
                max_age=30 * 24 * 60 * 60,  # 30 days
                httponly=True,
                samesite="lax"
            )

        return response

    except Exception as e:
        logger.error(
            "conversion_failed",
            converter_type="length",
            value=pyload.value,
            from_unit=pyload.from_unit,
            to_unit=pyload.to_unit,
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

    user_key, session_id, is_new = get_or_create_session(request)
    redis_service = RedisService(redis)

    history = await redis_service.get_history(
        user_key=user_key,
        converter_type="length"
    )

    return {"history": history}


@router.delete("/history")
async def clear_history(
        request: Request,
        redis: Redis = Depends(get_redis)
):
    """Clear conversion history."""

    user_key, session_id, is_new = get_or_create_session(request)
    redis_service = RedisService(redis)

    await redis_service.clear_history(
        user_key=user_key,
        converter_type="length"
    )

    return {"message": "History cleared"}