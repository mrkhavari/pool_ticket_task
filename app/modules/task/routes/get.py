from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.modules.task.schemas.get import TaskGetOutputSchema, TaskGetInputSchema
from app.modules.auth.models.user import User
from app.db.session import get_session
from app.modules.auth.helpers.get_current_user import get_current_user
from app.modules.task.helpers.get_task_by_id import get_task_by_id
from app.modules.task.helpers.filter_tasks import filter_tasks

router = APIRouter()


@router.get("/{task_id}", response_model=TaskGetOutputSchema)
async def get_task(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    task_id: Annotated[str, Path()],
) -> TaskGetOutputSchema:
    return await get_task_by_id(
        db=db,
        task_id=task_id,
    )


@router.get("/", response_model=list[TaskGetOutputSchema])
async def get_tasks(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_session)],
    obj_in: Annotated[TaskGetInputSchema, Query()],
) -> list[TaskGetOutputSchema]:
    return await filter_tasks(
        db=db,
        obj_in=obj_in,
    )
