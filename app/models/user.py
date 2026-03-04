from sqlalchemy import Column, String, Integer, UUID
from Base import BaseModel
from typing import Annotated
import uuid


class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)

    username = Column(String(12), nullable=False)
    password_hash = Column(String(60))
