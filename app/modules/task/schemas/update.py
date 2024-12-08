from pydantic import BaseModel, Field

from app.modules.task.schemas.task_status import TaskStatus
from app.core.constant_variables import STRING_LENGTH_32


class TaskUpdateOutputSchema(BaseModel):
    count: int


class TaskUpdateInputSchema(BaseModel):
    title: str | None = Field(max_length=STRING_LENGTH_32, default=None)
    description: str | None = None
    status: TaskStatus | None = None
