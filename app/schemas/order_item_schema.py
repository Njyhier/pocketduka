from .Baseschema import BaseSchema
from sqlalchemy import Numeric


class OrderItemCreate(BaseSchema):
    id: str
    product_id: str
    cart_id: str
    quantity: int
    price: float
    image_url: str
    order_id: str
