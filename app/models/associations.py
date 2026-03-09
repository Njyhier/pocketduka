from .Base import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class RolePermissions(BaseModel):
    __tablename__ = "role_permissions"

    role_id = Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"),primary_key=True)
    permission_id = Column(
        "permission_id", UUID(as_uuid=True), ForeignKey("permissions.id"),primary_key=True)
