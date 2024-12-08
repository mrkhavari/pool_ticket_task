from pydantic import BaseModel

from app.modules.task.schemas.task_status import TaskStatus


class TaskUpdateOutputSchema(BaseModel):
    count: int


class TaskUpdateInputSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
