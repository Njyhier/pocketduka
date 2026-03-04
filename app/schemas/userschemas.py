from Baseschema import BaseShema
from typing import Optional
from pydantic import Field, EmailStr
import uuid


class UserWrite(BaseShema):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserReadPrivate(BaseShema):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str


class UserReadPublic(BaseShema):
    first_name: str
    last_name: str


class UserUpdate(BaseShema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
