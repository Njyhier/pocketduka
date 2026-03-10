from .Base import BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer


class RolePermissions(BaseModel):
    __tablename__ = "role_permissions"
    id= Column(Integer)
    role_id = Column('role_id',String(60), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column('permission_id',String(60), ForeignKey("permissions.id"), primary_key=True)
