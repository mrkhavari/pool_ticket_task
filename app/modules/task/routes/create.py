from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.task.schemas.create import (
    TaskCreateInputSchema,
    TaskCreateOutputSchema,
)
from app.db.session import get_session
from app.modules.auth.models.user import User
from app.modules.auth.helpers.get_current_user import get_current_user
from app.modules.task.helpers.add_task import add_task

router = APIRouter()


@router.post("/", response_model=TaskCreateOutputSchema)
async def create_task(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    obj_in: TaskCreateInputSchema,
) -> TaskCreateOutputSchema:
    return await add_task(
        db=db,
        obj_in=obj_in,
    )
