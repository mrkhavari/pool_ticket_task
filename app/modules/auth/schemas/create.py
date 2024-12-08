from pydantic import BaseModel, Field

from app.core.constant_variables import STRING_LENGTH_32

class UserCreateInputSchema(BaseModel):
    username: str = Field(max_length=STRING_LENGTH_32)
    password: str


class UserCreateOutputSchema(BaseModel):
    id: str
    username: str
