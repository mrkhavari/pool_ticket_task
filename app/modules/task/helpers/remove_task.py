from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.task.schemas.delete import TaskDeleteOutputSchema
from app.modules.task.dals.task_dal import TaskDAL
from app.modules.task.models.task import Task
from app.core.constant_variables import TASK_NOT_FOUND, TASKS_CACHE_NAME
from app.cache.remove_cache_key import remove_cache_key


async def remove_task(
    db: Session,
    task_id: str,
) -> TaskDeleteOutputSchema:
    task: Optional[Task] = await TaskDAL(db).get(obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TASK_NOT_FOUND,
        )
    count: int = await TaskDAL(db).remove(
        obj_id=task_id,
        autocommit=True,
    )
    await remove_cache_key(prefix=TASKS_CACHE_NAME)
    return TaskDeleteOutputSchema(
        count=count,
    )
