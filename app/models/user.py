from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .Base import BaseModel
from datetime import datetime, timezone
import uuid


class User(BaseModel):
    __tablename__ = "users"

    id = Column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    username = Column(String(60), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    password_hash = Column(String(60), nullable=False)
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    addresses = relationship(
        "Address",
        back_populates="user",
        passive_deletes=True,
        cascade="all, delete-orphan",
    )
