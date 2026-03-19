from .Baseschema import BaseSchema
from typing import Optional

class AddressCreate(BaseSchema):
  address: str
  county: str
  city: str
  street: str
  ward: str

class Addressread(BaseSchema):
  address: str
  county: str
  city: str
  street: str
  ward: str

class AddressUpdate():
  address: Optional[str]
  county: Optional[str]
  city: Optional[str]
  street: Optional[str]
  ward: Optional[str]