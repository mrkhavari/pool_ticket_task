from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.schemas.create import UserCreateInputSchema, UserCreateOutputSchema
from app.modules.auth.models.user import User
from app.modules.auth.dals.user_dal import UserDAL
from app.core.constant_variables import INCORRECT_USERNAME

async def add_user(
    db: Session,
    obj_in: UserCreateInputSchema,
) -> UserCreateOutputSchema:
    existed_user: Optional[User] = await UserDAL(db).get_by_username(
        username=obj_in.username,
    )
    if existed_user:
        raise HTTPException(
            detail=INCORRECT_USERNAME,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user: User = await UserDAL(db).create(
        obj_in=obj_in,
    )
    return user