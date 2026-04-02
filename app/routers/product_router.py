from fastapi import APIRouter, Depends, Query
from app.schemas.product_schemas import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
)
from app.schemas.Baseschema import ApiResponse
from app.models.user import User
from app.services.auth_service import get_current_user
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


@router.post("/products", response_model=ApiResponse)
async def create_product_route(
    product_create: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_product(product_create, session)
    return {
        "status": 201,
        "message": "Product created successfully",
        "payload": payload,
    }


@router.get("/products", response_model=ApiResponse[list[ProductRead]])
async def read_products_route(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    _: User = Depends(get_current_user),
):
    payload = await read_products(
        session,
        skip=skip,
        limit=limit,
    )
    return {
        "status": 200,
        "message": "Products retrieved successfully",
        "payload": payload,
    }


@router.get("/products/{product_id}", response_model=ProductRead)
async def read_product_route(
    product_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await read_product(product_id, session)
    return {
        "status": 200,
        "message": "Product retrieved successfully",
        "payload": payload,
    }


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
