from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseSchema(BaseModel):
    class Config:
        from_orm = True


class DeleteResponce(BaseSchema):
    message: str


class ApiResponse(BaseSchema, Generic[T]):
    message: str
    payload: T
