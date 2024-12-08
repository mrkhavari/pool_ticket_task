from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.modules.auth.schemas.login import UserLoginInputForm, UserLoginOutputSchema
from app.db.session import get_session
from app.modules.auth.models.user import User
from app.modules.auth.helpers.authenticate_user import authenticate_user
from app.core.config import get_settings
from app.modules.auth.helpers.create_access_token import create_access_token

router = APIRouter()


@router.post("/login", response_model=UserLoginOutputSchema)
async def login(
    db: Annotated[Session, Depends(get_session)],
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> UserLoginOutputSchema:
    user: User = await authenticate_user(
        db=db,
        obj_in=UserLoginInputForm(
            username=form_data.username,
            password=form_data.password,
        ),
    )
    access_token_expires = timedelta(
        minutes=get_settings().USER_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        obj_in={"user_id": str(user.id)},
        expires_delta=access_token_expires,
    )
    return UserLoginOutputSchema(
        access_token=access_token,
        expires_in=str(
            datetime.now()
            + timedelta(minutes=get_settings().USER_ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
    )
