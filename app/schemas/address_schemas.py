from .Baseschema import BaseSchema
from typing import Optional


class AddressCreate(BaseSchema):
    address: str
    county: str
    city: str
    street: str
    ward: str


class AddressRead(BaseSchema):
    id: str
    address: str
    county: str
    city: str
    street: str
    ward: str


class AddressUpdate(BaseSchema):
    address: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    ward: Optional[str] = None
