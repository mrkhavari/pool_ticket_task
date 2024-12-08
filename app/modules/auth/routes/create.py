from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.auth.schemas.create import (
    UserCreateInputSchema,
    UserCreateOutputSchema,
)
from app.db.session import get_session
from app.modules.auth.helpers.add_user import add_user

router = APIRouter()


@router.post("/create", response_model=UserCreateOutputSchema)
async def create_user(
    db: Annotated[Session, Depends(get_session)],
    obj_in: UserCreateInputSchema,
) -> UserCreateOutputSchema:
    return await add_user(
        db=db,
        obj_in=obj_in,
    )
