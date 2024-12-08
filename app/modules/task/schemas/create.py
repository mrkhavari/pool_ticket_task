from pydantic import BaseModel

from app.modules.task.schemas.task_status import TaskStatus


class TaskCreateInputSchema(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.PENDING
    description: str | None = None


class TaskCreateOutputSchema(BaseModel):
    id: str
    title: str
    status: TaskStatus
    description: str | None = None
