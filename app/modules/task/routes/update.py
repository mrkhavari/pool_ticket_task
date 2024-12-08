from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.modules.task.schemas.update import (
    TaskUpdateOutputSchema,
    TaskUpdateInputSchema,
)
from app.modules.auth.models.user import User
from app.db.session import get_session
from app.modules.auth.helpers.get_current_user import get_current_user
from app.modules.task.helpers.refresh_task import refresh_task

router = APIRouter()


@router.patch("/{task_id}", response_model=TaskUpdateOutputSchema)
async def update_task(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    task_id: Annotated[str, Path()],
    obj_in: TaskUpdateInputSchema,
) -> TaskUpdateOutputSchema:
    return await refresh_task(
        db=db,
        task_id=task_id,
        obj_in=obj_in,
    )
