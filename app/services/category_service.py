from app.schemas.category_schemas import (
    CategoryCreate,
    CategoryUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.services.auth_service import get_current_user
from app.models.category import Category
from sqlalchemy import select


async def get_category_by_id(
    category_id: str,
    session: AsyncSession,
) -> Category:
    result = await session.execute(
        select(Category).where(Category.id == category_id),
    )
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


async def read_categories(session):
    result = await session.execute(select(Category))
    categories = result.scalars()
    return categories


async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession,
) -> Category:
    db_category = Category(**category_data.model_dump())
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


async def delete_category(category_id: str, session: AsyncSession):
    category_to_delete = await get_category_by_id(
        category_id=category_id, session=session
    )
    await session.delete(category_to_delete)
    await session.commit()
    return {"message": "Category deleted successfully"}


async def update_category(
    category_id: str,
    update_data: CategoryUpdate,
    session: AsyncSession,
):
    category_to_update = await get_category_by_id(
        category_id=category_id,
        session=session,
    )
    update_data = update_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    for key, value in update_data.items():
        setattr(category_to_update, key, value)
    await session.commit()
    await session.refresh(category_to_update)
    return category_to_update
