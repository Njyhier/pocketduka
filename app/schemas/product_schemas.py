from pydantic import Field
from typing import Optional
from .Baseschema import BaseSchema
from decimal import Decimal
import uuid


class ProductBase(BaseSchema):
    name: str
    price: Decimal
    description: str
    category: str


class ProductRead(ProductBase):
    id: uuid.UUID


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    category: Optional[str] = None


class DeleteResponce(BaseSchema):

    message: str
