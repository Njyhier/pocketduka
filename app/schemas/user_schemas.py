from .Baseschema import BaseSchema
from typing import Optional
from pydantic import Field, EmailStr
import uuid


class UserWrite(BaseSchema):
    email: str
    username: str
    password: str


class UserSignUp(BaseSchema):
    email: str
    username: str
    password: str


class UserReadPrivate(BaseSchema):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    role_names: list[str]


class UserReadPublic(BaseSchema):
    first_name: str
    last_name: str


class UserUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
