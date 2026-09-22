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


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int
