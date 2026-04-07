from sqlalchemy import Column, String, DateTime, Text, Numeric, ForeignKey
from .Base import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.models.product_image import ProductImage

import uuid


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name = Column(String)
    price = Column(Numeric(10, 2))
    description = Column(Text)
    category_name = Column(
        String,
        ForeignKey("categories.name"),
    )
    category = relationship(
        "Category",
        back_populates="products",
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    inventories = relationship(
        "Inventory",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    cart_items = relationship(
        "CartItem",
        back_populates="product",
    )
