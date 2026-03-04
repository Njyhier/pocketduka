from pydantic import BaseModel


class BaseShema(BaseModel):
    class Config:
        from_orm = True
