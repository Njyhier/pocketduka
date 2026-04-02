from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class ApiResponse(BaseSchema, Generic[T]):
    status: Optional[int]
    message: Optional[str]
    payload: Optional[T]
