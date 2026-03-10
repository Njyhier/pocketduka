from .Baseschema import BaseSchema
from typing import Optional


class BaseRole(BaseSchema):
    id: str
    name: str


class RoleCreate(BaseSchema):
    name: str
