from .Baseschema import BaseSchema
from datetime import datetime


class OrderRead(BaseSchema):
    id: str
    status: str
    created_at: datetime
    total_amount: float
