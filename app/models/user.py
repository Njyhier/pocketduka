from sqlalchemy import Column, String, Integer, UUID as SQLUUID
from .Base import BaseModel
from typing import Annotated
import uuid


class User(BaseModel):
    __tablename__ = "users"

    id = Column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    username = Column(String(12), nullable=False)
    password_hash = Column(String(60))
