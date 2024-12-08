from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.task.schemas.get import TaskGetOutputSchema, TaskGetInputSchema
from app.modules.task.models.task import Task
from app.modules.task.dals.task_dal import TaskDAL
from app.cache.cache_response_decorator import cache_response
from app.core.constant_variables import TASKS_CACHE_NAME


@cache_response(
    cache_name=TASKS_CACHE_NAME,
)
async def filter_tasks(
    db: Session,
    obj_in: TaskGetInputSchema,
) -> list[TaskGetOutputSchema]:
    tasks: list[Task] = await TaskDAL(db).filter_by_user_query(
        obj_in=obj_in,
    )
    return [
        TaskGetOutputSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=int(datetime.timestamp(task.created_at)),
        )
        for task in tasks
    ]
