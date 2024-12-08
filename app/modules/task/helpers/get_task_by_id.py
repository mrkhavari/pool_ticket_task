from typing import Optional
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.task.schemas.get import TaskGetOutputSchema
from app.modules.task.dals.task_dal import TaskDAL
from app.modules.task.models.task import Task
from app.core.constant_variables import TASK_NOT_FOUND


async def get_task_by_id(
    db: Session,
    task_id: str,
) -> TaskGetOutputSchema:
    task: Optional[Task] = await TaskDAL(db).get(obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TASK_NOT_FOUND,
        )

    return TaskGetOutputSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=int(datetime.timestamp(task.created_at)),
    )
