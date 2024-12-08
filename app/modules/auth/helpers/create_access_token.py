from datetime import datetime, timedelta
from typing import Any, Dict

import jwt

from app.core.config import get_settings


def create_access_token(obj_in: Dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = obj_in.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        payload=to_encode,
        key=get_settings().JWT_SECRET_KEY,
        algorithm=get_settings().JWT_ALGORITHM,
    )
    return encoded_jwt
