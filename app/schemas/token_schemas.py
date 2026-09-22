from .Baseschema import BaseModel
from .user_schemas import UserReadPrivate


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserReadPrivate


class TokenData(BaseModel):
    username: str | None = None
    id: str | None = None
