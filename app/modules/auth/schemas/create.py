from pydantic import BaseModel


class UserCreateInputSchema(BaseModel):
    username: str
    password: str


class UserCreateOutputSchema(BaseModel):
    id: str
    username: str
