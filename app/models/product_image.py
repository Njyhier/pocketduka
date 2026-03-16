from sqlalchemy import Column, String, DateTime, Text, Numeric, Boolean, ForeignKey
from .Base import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

import uuid


class ProductImage(BaseModel):
    __tablename__ = "product_images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, unique=True, nullable=False)
    file_name = Column(String, unique=True, nullable=False)
    is_main = Column(Boolean, default=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now(timezone.utc))
    product = relationship("Product", back_populates="images")
