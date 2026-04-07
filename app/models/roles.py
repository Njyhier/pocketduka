from .Base import BaseModel
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from datetime import datetime, timezone
import uuid


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc)
    )
    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
    users = relationship("User", secondary="user_roles", back_populates="roles")
