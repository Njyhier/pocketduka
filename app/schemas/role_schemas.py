from .Baseschema import BaseSchema
from typing import Optional


class BaseRole(BaseSchema):
    id: str
    name: str
    permissions: list[str]


class RoleCreate(BaseSchema):
    name: str
    permissions: Optional[list[str]]


class RoleUpdate(BaseSchema):
    permissions: Optional[list[str]] = None


class RoleRead(BaseSchema):
    id: str
    name: str


class UserRoleUpdate(BaseSchema):
    role_names: set[str]
