from .Baseschema import BaseSchema
from app.schemas.cart_item_schema import CartItemRead


class CartRead(BaseSchema):
    id: str
    items: list[CartItemRead]
    user_id: str
    subtotal: float
    total_items: int
