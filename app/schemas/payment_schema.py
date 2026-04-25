from .Baseschema import BaseSchema
from typing import Optional


class PaymentCreate(BaseSchema):
    phone_number: str
    checkout_request_id: str
    merchant_request_id: str
    order_id: str
    user_id: str
    amount: str


class PaymentRead(BaseSchema):
    phone_number: str
    amount: str
    status: str
    mpesa_receipt_number: Optional[str]
    checkout_request_id: Optional[str]
    merchant_request_id: str
    result_code: str
    result_desc: str
    order_id: str
    user_id: str
    item: Optional[dict]


class Data(BaseSchema):
    order_id: str
    user_id: str
    phone_number: str
