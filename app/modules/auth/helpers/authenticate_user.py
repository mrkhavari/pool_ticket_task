from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.auth.schemas.login import UserLoginInputForm
from app.modules.auth.models.user import User
from app.modules.auth.dals.user_dal import UserDAL
from app.core.constant_variables import USERNAME_NOT_FOUND, INCORRECT_PASSWORD
from app.modules.auth.helpers.verify_password import verify_password


async def authenticate_user(
    db: Session,
    obj_in: UserLoginInputForm,
) -> User:
    user: Optional[UserDAL] = await UserDAL(db=db).get_by_username(
        username=obj_in.username,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USERNAME_NOT_FOUND,
        )
    if not verify_password(obj_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=INCORRECT_PASSWORD
        )
    return user
