from .Baseschema import BaseSchema


class ImageCreate(BaseSchema):
    url: str
    file_name: str
    product_id: str


class PostImageSuccess(BaseSchema):
    message: str


class ImageRead(BaseSchema):
    url: str
    file_name: str
    product_id: str
