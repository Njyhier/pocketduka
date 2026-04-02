from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schemas.Baseschema import ApiResponse
from app.schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryRead
from app.services.category_service import (
    create_category,
    get_category_by_id,
    delete_category,
    update_category,
    read_categories,
)

router = APIRouter()


@router.post("/categories", response_model=ApiResponse[CategoryRead])
async def add_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_category(category_data=category_data, session=session)
    return {
        "message": "Category added successfully",
        "payload": payload,
    }


@router.get("/categories", response_model=ApiResponse[list[CategoryRead]])
async def get_categories(
    session: AsyncSession = Depends(get_async_session),
):
    categories = await read_categories(session=session)
    return {
        "message": "Categories retrieved successfully",
        "payload": categories,
    }


@router.get("/categories/{category_id}", response_model=ApiResponse[CategoryRead])
async def read_category_by_id(
    category_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    category = await get_category_by_id(category_id=category_id, session=session)
    return {
        "message": "Retrieve category successful",
        "payload": category,
    }


@router.patch("/categories/{category_id}", response_model=ApiResponse[CategoryRead])
async def patch_category(
    category_id: str,
    category_data: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await update_category(
        category_id=category_id,
        update_data=category_data,
        session=session,
    )
    return {
        "message": "Category updated successfully",
        "payload": payload,
    }


@router.delete("/categories/{category_id}", response_model=ApiResponse)
async def remove_category(
    category_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_category(category_id=category_id, session=session)
