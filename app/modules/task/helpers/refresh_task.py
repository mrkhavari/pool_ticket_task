from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.task.schemas.update import (
    TaskUpdateOutputSchema,
    TaskUpdateInputSchema,
)
from app.modules.task.dals.task_dal import TaskDAL
from app.modules.task.models.task import Task
from app.core.constant_variables import TASK_NOT_FOUND, INCORRECT_TITLE, TASKS_CACHE_NAME
from app.cache.remove_cache_key import remove_cache_key

async def refresh_task(
    db: Session,
    task_id: str,
    obj_in: TaskUpdateInputSchema,
) -> TaskUpdateOutputSchema:
    task: Optional[Task] = await TaskDAL(db).get(obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TASK_NOT_FOUND,
        )
    if obj_in.title and obj_in.title != task.title:
        existed_task: Optional[Task] = await TaskDAL(db).get_by_title(
            title=obj_in.title,
        )
        if existed_task:
            raise HTTPException(
                detail=INCORRECT_TITLE,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    count: int = await TaskDAL(db).update_task(
        task_id=task_id,
        obj_in=obj_in,
        autocommit=True,
    )
    await remove_cache_key(prefix=TASKS_CACHE_NAME)
    return TaskUpdateOutputSchema(
        count=count,
    )
