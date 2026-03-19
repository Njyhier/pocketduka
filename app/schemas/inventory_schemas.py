from .Baseschema import BaseSchema
from typing import Optional


class InventoryCreate():
  product_id: str
  quantity: int
  reserved_quantity: Optional[str]
  location: str

class InventoryRead(BaseSchema):
  product_id: str
  quantity: int
  reserved_quantity: Optional[str]
  location: str

class InventoryUpdate(BaseSchema):
  product_id: Optional[str]
  quantity: Optional[int]
  reserved_quantity: Optional[str]
  location: Optional[str]


