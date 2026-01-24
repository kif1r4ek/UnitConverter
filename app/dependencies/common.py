from fastapi.templating import Jinja2Templates
from fastapi import Request
from pint import UnitRegistry

from app.core.logger import get_logger

templates = Jinja2Templates(directory="app/views/templates")

ureg = UnitRegistry()

logger = get_logger(__name__)

def get_user_key(request: Request) -> str:
    """
    Generate unique user key for history.

    Uses session ID from cookie or creates new one.
    In production, use authenticated user_id.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())

    return f"session:{session_id}"

def get_or_create_session(request: Request) -> tuple[str, str, bool]:
    """
    Get or create session for user.

    Returns:
        tuple: (user_key, session_id, is_new_session)
    """
    session_id = request.cookies.get("session_id")
    is_new = False

    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())
        is_new = True

    user_key = f"session:{session_id}"
    return user_key, session_id, is_new
