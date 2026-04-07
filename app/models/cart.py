from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from .Base import BaseModel
import uuid
from datetime import datetime, timezone


class Cart(BaseModel):
    __tablename__ = "carts"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    items = relationship(
        "CartItem",
        back_populates="cart",
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        unique=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user = relationship(
        "User",
        back_populates="cart",
    )
    orders = relationship("Order", back_populates="cart")

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)

    @property
    def total_items(self) -> Integer:
        items = [item.quantity for item in self.items]
        return sum(items)
