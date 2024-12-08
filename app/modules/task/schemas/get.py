from datetime import datetime
from pydantic import BaseModel, Field

from app.modules.task.schemas.task_status import TaskStatus
from app.core.constant_variables import MAX_TASK_QUERY


class TaskGetOutputSchema(BaseModel):
    id: str
    title: str
    status: TaskStatus
    created_at: int
    description: str | None = None


class TaskGetInputSchema(BaseModel):
    skip: int = 0
    limit: int = Field(le=MAX_TASK_QUERY, default=MAX_TASK_QUERY)
    status: TaskStatus | None = None
    created_at: int | None = None
