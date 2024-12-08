from pydantic import BaseModel, Field

from app.core.constant_variables import STRING_LENGTH_32

class UserLoginInputForm(BaseModel):
    username: str = Field(max_length=STRING_LENGTH_32)
    password: str


class UserLoginOutputSchema(BaseModel):
    access_token: str
    expires_in: str
    token_type: str | None = "Bearer"
