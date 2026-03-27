from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from uuid import uuid4
from .Base import BaseModel  # assuming you have a base class


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    products = relationship(
        "Product",
        back_populates="category",
    )
