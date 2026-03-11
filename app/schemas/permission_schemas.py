from .Baseschema import BaseSchema
from typing import Optional


class PermissionCreate(BaseSchema):
    name: str
    action: str
    target: str


class PermissionRead(PermissionCreate):
    id: str


class PermissionUpdate(BaseSchema):
    name: Optional[str] = None
    action: Optional[str] = None
    target: Optional[str] = None
