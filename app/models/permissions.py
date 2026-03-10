from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .Base import BaseModel
from .associations import RolePermissions
import uuid


class Permission(BaseModel):
    __tablename__ = "permissions"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), nullable=False)
    action = Column(String(15), nullable=False)
    target = Column(String(15), nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    roles = relationship(
        "Role", secondary="role_permissions", back_populates="permissions"
    )
