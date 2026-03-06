from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_orm = True
