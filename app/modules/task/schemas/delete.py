from pydantic import BaseModel


class TaskDeleteOutputSchema(BaseModel):
    count: int