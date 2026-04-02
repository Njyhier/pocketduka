from .Baseschema import BaseSchema
from typing import Optional


class CartItemRead(BaseSchema):
    id: str
    name: str
    quantity: int
    price: float
    category: str
    subtotal: float
    image_url: Optional[str]
