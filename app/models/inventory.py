from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .Base import BaseModel
from datetime import datetime, timezone
import uuid
from sqlalchemy import Numeric


class Inventory(BaseModel):
    __tablename__ = "inventories"

    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    product_id = Column(
        String(60),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    product = relationship("Product", back_populates="inventories")
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime,
        onupdate=lambda: datetime.now(timezone.utc),
    )
    location = Column(String(60), nullable=True, unique=True)
