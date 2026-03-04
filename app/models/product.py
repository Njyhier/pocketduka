from sqlalchemy import Column, String, UUID, Integer, Text, Numeric
from Base import BaseModel
import uuid


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    price = Column(Numeric(10, 2))
    description = Column(Text)
    category = Column(String)
