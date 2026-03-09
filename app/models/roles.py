from Base import BaseModel
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), nullable=False)

    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
