from pydantic import BaseModel
from typing import TypeVar, Any

T = TypeVar("T")


class BaseSchema(BaseModel):
    class Config:
        from_orm = True


class DeleteResponce(BaseSchema):
    message: str


class ApiResponse(BaseSchema):
    message: str
    payload: Any
