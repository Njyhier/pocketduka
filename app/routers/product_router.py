from fastapi import APIRouter, Depends
from app.schemas.product_schemas import ProductRead, ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.product_service import (
    create_product,
    read_products,
    read_product,
    delete_product,
    update_product,
)

router = APIRouter()


@router.post("/products", response_model=ProductRead)
async def create_product_route(
    product_create: ProductCreate, session: AsyncSession = Depends(get_async_session)
):
    return await create_product(product_create, session)


@router.get("/products")
async def read_products_route(session: AsyncSession = Depends(get_async_session)):
    return await read_products(session)


@router.get("/products/{product_id}", response_model=ProductRead)
async def read_product_route(
    product_id: str, session: AsyncSession = Depends(get_async_session)
):
    return await read_product(product_id, session)


@router.delete("/products/{product_id}")
async def delete_product_route(
    product_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_product(product_id, session)


@router.patch("/products/{id}", response_model=ProductRead)
async def patch_product_route(
    update_data: ProductUpdate,
    id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_product(id, update_data, session)
