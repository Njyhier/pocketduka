from .Base import BaseModel
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="Pending")
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime,
        onupdate=lambda: datetime.now(timezone.utc),
    )
    items = relationship("OrderItem", back_populates="order")
    cart_id = Column(
        String(60),
        ForeignKey("carts.id"),
        nullable=False,
    )
    cart = relationship("Cart", back_populates="orders")

    def update_status(self):
        if self.status == "Delivered":
            return
        if self.status == "Pending":
            self.status = "In transit"
            return
        if self.status == "In transit":
            self.status = "Delivered"
            return
