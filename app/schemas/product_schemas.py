from pydantic import Field
from typing import Optional
from .Baseschema import BaseSchema
from decimal import Decimal
import uuid


class ProductBase(BaseSchema):
    name: str
    price: Decimal
    description: str


class ProductRead(ProductBase):
    id: uuid.UUID


class ProductCreate(ProductBase):
    category_id: Optional[str]


class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    category: Optional[str] = None


class DeleteResponce(BaseSchema):

    message: str
