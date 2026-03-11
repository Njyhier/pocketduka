from .Baseschema import BaseSchema
from typing import Optional
from pydantic import Field, EmailStr
import uuid


class UserWrite(BaseSchema):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    username: str
    password: str


class UserReadPrivate(BaseSchema):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str


class UserReadPublic(BaseSchema):
    first_name: str
    last_name: str


class UserUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
