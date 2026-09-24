# from fastapi import APIRouter, Depends, Query
# from app.schemas.product_schemas import (
#     ProductRead,
#     ProductCreate,
#     ProductUpdate,
#     ProductCreateRead,
# )
# from app.schemas.Baseschema import ApiResponse
# from app.models.user import User

# # from app.services.auth_service import get_current_user
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import get_async_session

# from app.middlewares.rbac_middleware import SystemTasks

# # from app.routers.rbac_routes import RBACRoute
# from app.services.product_service import (
#     create_product,
#     read_products,
#     read_product,
#     delete_product,
#     update_product,
# )

# router = APIRouter()


# @router.post("/products")
# # @SystemTasks("create_products")
# async def create_product_route(
#     product_create: ProductCreate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     payload = await create_product(product_create, session)
#     return {
#         "status": 201,
#         "message": "Product created successfully",
#         "payload": payload,
#     }


# @router.get("/products", response_model=ApiResponse[list[ProductRead]])
# async def read_products_route(
#     session: AsyncSession = Depends(get_async_session),
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, ge=1),
# ):
#     payload = await read_products(
#         session,
#         skip=skip,
#         limit=limit,
#     )
#     return {
#         "status": 200,
#         "message": "Products retrieved successfully",
#         "payload": payload,
#     }


# @router.get("/products/{product_id}", response_model=ApiResponse[ProductRead])
# async def read_product_route(
#     product_id: str,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     payload = await read_product(product_id, session)
#     return {
#         "status": 200,
#         "message": "Product retrieved successfully",
#         "payload": payload,
#     }


# @router.delete("/products/{product_id}")
# @SystemTasks("delete_products")
# async def delete_product_route(
#     product_id: str,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     return await delete_product(product_id, session)


# @router.patch("/products/{id}", response_model=ProductRead)
# @SystemTasks("update_products")
# async def patch_product_route(
#     update_data: ProductUpdate,
#     id: str,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     return await update_product(id, update_data, session)

from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.middlewares.rbac_middleware import SystemTasks
from app.schemas.Baseschema import PaginatedResponse, ApiResponse
from app.schemas.product_schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from app.services.product_service import (
    create_product,
    delete_product,
    read_product,
    read_products,
    update_product,
)

router = APIRouter()


@router.post("/products")
# @SystemTasks("create_products")
async def create_product_route(
    product_create: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
):
    product = await create_product(
        product_data=product_create,
        session=session,
    )

    return {
        "status": 201,
        "message": "Product created successfully",
        "payload": product,
    }


@router.get(
    "/products",
    response_model=PaginatedResponse[ProductRead],
)
async def read_products_route(
    session: AsyncSession = Depends(get_async_session),
    # Pagination
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of products to skip",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of products to return",
    ),
    # Search
    search: str | None = Query(
        default=None,
        min_length=1,
        description="Search by product name or description",
    ),
    # Filters
    category: str | None = Query(
        default=None,
        description="Filter products by category",
    ),
    min_price: Decimal | None = Query(
        default=None,
        ge=0,
        description="Minimum product price",
    ),
    max_price: Decimal | None = Query(
        default=None,
        ge=0,
        description="Maximum product price",
    ),
    in_stock: bool | None = Query(
        default=None,
        description="Return only products currently in stock",
    ),
    # Sorting
    sort_by: str = Query(
        default="created_at",
        description="Sort by: name, price, created_at, id",
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort direction: asc or desc",
    ),
):
    products = await read_products(
        session=session,
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return products


@router.get(
    "/products/{product_id}",
    response_model=ApiResponse[ProductRead],
)
async def read_product_route(
    product_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    product = await read_product(
        product_id=product_id,
        session=session,
    )

    return {
        "status": 200,
        "message": "Product retrieved successfully",
        "payload": product,
    }


@router.patch(
    "/products/{product_id}",
    response_model=ProductRead,
)
@SystemTasks("update_products")
async def patch_product_route(
    product_id: str,
    update_data: ProductUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_product(
        product_id=product_id,
        update_data=update_data,
        session=session,
    )


@router.delete("/products/{product_id}")
@SystemTasks("delete_products")
async def delete_product_route(
    product_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_product(
        product_id=product_id,
        session=session,
    )
