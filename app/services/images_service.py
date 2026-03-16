from fastapi import UploadFile, HTTPException, status
from app.schemas.product_image_schemas import ImageCreate, PostImageSuccess
from imagekitio import ImageKit
from sqlalchemy.ext.asyncio import AsyncSession
import os
from app.models.product_image import ProductImage
from dotenv import load_dotenv

load_dotenv()

imageKit = ImageKit(private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"))
# url_endpoint = os.getenv("IMAGEKIT_URL_ENDPOINT")


async def create_product_image(product_id: str, image_data: UploadFile) -> ProductImage:
    file = await image_data.read()
    if not file:
        raise
    response = imageKit.files.upload(
        file=file,
        file_name=image_data.filename,
        folder="/product_images",
    )

    return ProductImage(
        url=response.url,
        file_name=image_data.filename,
        product_id=product_id,
    )


async def add_image_to_db(
    product_id: str, image: ImageCreate, session: AsyncSession
) -> PostImageSuccess:
    db_image = await create_product_image(
        product_id=product_id,
        image_data=image,
    )
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    return {"message": "Image added successfully"}
