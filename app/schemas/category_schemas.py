from .Baseschema import BaseSchema
from typing import Optional


class CategoryCreate(BaseSchema):
    name: str
    descripion: str


class CategoryRead(BaseSchema):
    name: str
    description: str


class CategoryUpdate(BaseSchema):
    name: Optional[str]
    description: Optional[str]
