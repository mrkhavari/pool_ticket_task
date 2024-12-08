from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.task.schemas.create import (
    TaskCreateOutputSchema,
    TaskCreateInputSchema,
)
from app.modules.task.models.task import Task
from app.modules.task.dals.task_dal import TaskDAL
from app.core.constant_variables import INCORRECT_TITLE, TASKS_CACHE_NAME
from app.cache.remove_cache_key import remove_cache_key
from app.celery.tasks import send_email_notification


async def add_task(
    db: Session,
    obj_in: TaskCreateInputSchema,
) -> TaskCreateOutputSchema:
    existed_task: Optional[Task] = await TaskDAL(db).get_by_title(
        title=obj_in.title,
    )
    if existed_task:
        raise HTTPException(
            detail=INCORRECT_TITLE,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    task: Task = await TaskDAL(db).create(
        obj_in=obj_in,
    )

    await remove_cache_key(prefix=TASKS_CACHE_NAME)

    send_email_notification.delay(task.title)

    return task
