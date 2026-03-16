from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.images_service import add_image_to_db, PostImageSuccess
from typing import Annotated

router = APIRouter()


@router.post("/upload_image", response_model=PostImageSuccess)
async def upload_image(
    product_id: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    image: UploadFile | None = File(None),
):

    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded",
        )
    return await add_image_to_db(
        product_id=product_id,
        image=image,
        session=session,
    )
