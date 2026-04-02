from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel
import uuid
from datetime import datetime, timezone


class CartItem(BaseModel):
    __tablename__ = "cartitems"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    name = Column(String(60))
    product_id = Column(
        String(60),
        ForeignKey("products.id"),
    )
    product = relationship(
        "Product",
        back_populates="cart_items",
    )
    cart_id = Column(
        String(60),
        ForeignKey("carts.id"),
    )
    cart = relationship(
        "Cart",
        back_populates="items",
    )
    quantity = Column(
        Integer,
        nullable=False,
        default=1,
    )
    price = Column(
        Numeric(10, 2),
        nullable=False,
    )
    category = Column(String(60))

    image_url = Column(
        String,
        nullable=True,
    )

    @property
    def subtotal(self):
        return self.price * self.quantity

    def increment_quantity(self):
        self.quantity += 1

    def decrement_quantity(self):
        self.quantity -= 1
