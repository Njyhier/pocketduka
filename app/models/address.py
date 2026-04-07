from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .Base import BaseModel
from datetime import datetime, timezone
import uuid


class Address(BaseModel):
    __tablename__ = "addresses"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    users = relationship(
        "User",
        secondary="user_addresses",
        back_populates="addresses",
    )
    city = Column(String(150), nullable=True)
    county = Column(String, nullable=True)
    ward = Column(String, nullable=True)
    street = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    address = Column(String(60), nullable=True)
