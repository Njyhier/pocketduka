from .Baseschema import BaseSchema
from typing import Optional


class CategoryCreate(BaseSchema):
    name: str
    description: str


class CategoryRead(BaseSchema):
    name: str
    description: str
    id: str

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
