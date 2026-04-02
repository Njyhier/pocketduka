from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from .Base import BaseModel
import uuid
from datetime import datetime, timezone


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
    )
    product_id = Column(
        String(60),
    )
    quantity = Column(
        Integer,
        nullable=False,
    )
    price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    image_url = Column(
        String,
        nullable=True,
    )
    order_id = Column(
        String(60),
        ForeignKey("orders.id"),
        nullable=True,
    )
    order = relationship(
        "Order",
        back_populates="items",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def subtotal(self):
        return self.price * self.quantity
