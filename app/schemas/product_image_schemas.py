from .Baseschema import BaseSchema
from pydantic import FilePath, FileUrl


class ImageCreate(BaseSchema):
    url: str
    file_name: str
    product_id: str


class PostImageSuccess(BaseSchema):
    message: str
