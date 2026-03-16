from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product_schemas import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
    DeleteResponce,
)
from app.models.product import Product
from sqlalchemy import select
from fastapi import HTTPException, status, Query


async def get_product_by_id(product_id: str, session: AsyncSession) -> Product:
    res = await session.execute(select(Product).where(Product.id == product_id))
    product = res.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
        )
    return product


async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product(**product_data.model_dump())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


async def update_product(
    product_id: str, update_data: ProductUpdate, session: AsyncSession
) -> Product:
    product_to_update = await get_product_by_id(product_id, session)
    product_update = update_data.model_dump(exclude_unset=True)
    for key, value in product_update.items():
        setattr(product_to_update, key, value)

    await session.commit()
    await session.refresh(product_to_update)
    return product_to_update


async def read_products(
    session: AsyncSession,
    skip: int,
    limit: int,
) -> list[ProductRead]:
    result = await session.execute(
        select(Product).offset(skip).limit(limit),
    )
    products = result.scalars().all()

    return products


async def read_product(product_id: str, session: AsyncSession) -> Product:
    product = await get_product_by_id(product_id, session)
    return product


async def delete_product(product_id: str, session: AsyncSession) -> dict:
    product_to_delete = await get_product_by_id(product_id, session)
    await session.delete(product_to_delete)
    await session.commit()
    return {"message": "Product deleted successfully"}
