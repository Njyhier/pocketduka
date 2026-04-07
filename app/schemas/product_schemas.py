from pydantic import Field
from typing import Optional
from .Baseschema import BaseSchema
from .product_image_schemas import ImageRead
from .inventory_schemas import InventoryRead
from decimal import Decimal
import uuid


class ProductBase(BaseSchema):
    name: str
    description: str


class ProductRead(ProductBase):
    id: uuid.UUID
    category_name: str
    images: list[ImageRead]
    inventories: list[InventoryRead]
    description: str


class ProductCreate(ProductBase):
    category_name: Optional[str]


class ProductCreateRead(ProductCreate):
    product_id: str


class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    category: Optional[str] = None


class DeleteResponce(BaseSchema):

    message: str
