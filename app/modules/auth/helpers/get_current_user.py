from typing import Annotated, Optional
import jwt

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modules.auth.models.user import User
from app.modules.auth.dals.user_dal import UserDAL
from app.db.session import get_session
from app.core.config import get_settings
from app.core.constant_variables import USERNAME_NOT_FOUND, INVALID_AUTHENTICATION

user_oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_session)],
    token: str = Depends(user_oauth2_schema),
) -> User:
    payload = jwt.decode(
        token,
        get_settings().JWT_SECRET_KEY,
        algorithms=[get_settings().JWT_ALGORITHM],
    )
    user_id: str = str(payload.get("user_id"))
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INVALID_AUTHENTICATION
        )
    user: Optional[User] = await UserDAL(db).get(
        obj_id=user_id
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USERNAME_NOT_FOUND
        )

    return user