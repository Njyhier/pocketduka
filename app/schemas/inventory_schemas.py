from .Baseschema import BaseSchema
from typing import Optional


class InventoryCreate(BaseSchema):
    product_id: str
    quantity: int
    reserved_quantity: int
    cost_price: float
    selling_price: float


class InventoryRead(BaseSchema):
    id: str
    product_id: str
    quantity: int
    reserved_quantity: int
    selling_price: float
    location: Optional[str]
    model_config = {"from_attributes": True}


class InventoryUpdate(BaseSchema):
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    location: Optional[str] = None
