from pydantic import BaseModel, Field

from app.modules.task.schemas.task_status import TaskStatus
from app.core.constant_variables import STRING_LENGTH_32

class TaskCreateInputSchema(BaseModel):
    title: str = Field(max_length=STRING_LENGTH_32)
    status: TaskStatus = TaskStatus.PENDING
    description: str | None = None


class TaskCreateOutputSchema(BaseModel):
    id: str
    title: str
    status: TaskStatus
    description: str | None = None
