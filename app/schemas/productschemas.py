from pydantic import Field
from Baseschema import BaseShema
from decimal import Decimal
import uuid


class ProductBase(BaseShema):
    name: str
    price: Decimal
    description: str
    category: str


class ProductRead(ProductBase):
    id: uuid.UUID
