# from sqlalchemy.ext.asyncio import AsyncSession
# from app.schemas.product_schemas import (
#     ProductCreate,
#     ProductUpdate,
#     ProductRead,
# )
# from sqlalchemy.orm import selectinload
# from app.models.product import Product
# from sqlalchemy import select
# from fastapi import HTTPException, status


# async def get_product_by_id(product_id: str, session: AsyncSession) -> Product:
#     res = await session.execute(
#         select(Product)
#         .options(
#             selectinload(Product.inventories),
#             selectinload(Product.images),
#             selectinload(Product.category),
#         )
#         .where(Product.id == product_id)
#     )
#     product = res.scalar_one_or_none()
#     if product is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
#         )
#     return product


# async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
#     db_product = Product(**product_data.model_dump())
#     session.add(db_product)
#     await session.commit()
#     await session.refresh(db_product)
#     return db_product.id


# async def update_product(
#     product_id: str, update_data: ProductUpdate, session: AsyncSession
# ) -> Product:
#     product_to_update = await get_product_by_id(product_id, session)
#     product_update = update_data.model_dump(exclude_unset=True)
#     for key, value in product_update.items():
#         setattr(product_to_update, key, value)

#     await session.commit()
#     await session.refresh(product_to_update)
#     return product_to_update


# async def read_products(
#     session: AsyncSession,
#     skip: int,
#     limit: int,
# ) -> list[ProductRead]:
#     result = await session.execute(
#         select(Product)
#         .offset(skip)
#         .limit(limit)
#         .options(selectinload(Product.images), selectinload(Product.inventories)),
#     )
#     products = result.scalars().all()

#     return products


# async def read_product(product_id: str, session: AsyncSession) -> Product:
#     product = await get_product_by_id(product_id, session)
#     return product


# async def delete_product(product_id: str, session: AsyncSession) -> dict:
#     product_to_delete = await get_product_by_id(product_id, session)
#     await session.delete(product_to_delete)
#     await session.commit()
#     return {
#         "status": 200,
#         "message": "Product deleted successfully",
#     }


# async def create_order_with_images():
#     pass


from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import asc, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.product_schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
)


async def get_product_by_id(
    product_id: str,
    session: AsyncSession,
) -> Product:
    result = await session.execute(
        select(Product)
        .options(
            selectinload(Product.inventories),
            selectinload(Product.images),
            selectinload(Product.category),
        )
        .where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found!",
        )

    return product


async def create_product(
    product_data: ProductCreate,
    session: AsyncSession,
) -> Product:
    product_values = product_data.model_dump()

    db_product = Product(**product_values)

    session.add(db_product)

    try:
        await session.commit()
        await session.refresh(db_product)

    except Exception:
        await session.rollback()
        raise

    return db_product


async def update_product(
    product_id: str,
    update_data: ProductUpdate,
    session: AsyncSession,
) -> Product:
    product = await get_product_by_id(
        product_id=product_id,
        session=session,
    )

    update_values = update_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    # ProductUpdate uses `category`,
    # while Product uses `category_name`.
    if "category" in update_values:
        update_values["category_name"] = update_values.pop("category")

    for field, value in update_values.items():
        setattr(product, field, value)

    try:
        await session.commit()
        await session.refresh(product)

    except Exception:
        await session.rollback()
        raise

    return product


from decimal import Decimal

from sqlalchemy import select, or_, asc, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product_schemas import ProductRead
from app.schemas.Baseschema import PaginatedResponse


async def read_products(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    category: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    in_stock: bool | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> PaginatedResponse[list[ProductRead]]:

    # -----------------------------------------
    # Pagination
    # -----------------------------------------

    skip = max(skip, 0)
    limit = min(max(limit, 1), 100)

    # -----------------------------------------
    # Filters
    # -----------------------------------------

    filters = []

    # Search by name or description
    if search:
        search_term = f"%{search.strip()}%"

        filters.append(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        )

    # Category filter
    if category:
        filters.append(Product.category_name.ilike(category.strip()))

    # Minimum price
    if min_price is not None:
        filters.append(Product.price >= min_price)

    # Maximum price
    if max_price is not None:
        filters.append(Product.price <= max_price)

    # Only products that have stock
    if in_stock is True:
        filters.append(Product.inventories.any(Inventory.quantity > 0))

    # -----------------------------------------
    # Count total matching products
    # -----------------------------------------

    count_query = select(func.count(Product.id)).where(*filters)

    count_result = await session.execute(count_query)

    total = count_result.scalar_one()

    # -----------------------------------------
    # Calculate pagination information
    # -----------------------------------------

    page = (skip // limit) + 1

    total_pages = (total + limit - 1) // limit

    # -----------------------------------------
    # Base query
    # -----------------------------------------

    query = (
        select(Product)
        .where(*filters)
        .options(
            selectinload(Product.images),
            selectinload(Product.inventories),
        )
    )

    # -----------------------------------------
    # Sorting
    # -----------------------------------------

    allowed_sort_fields = {
        "name": Product.name,
        "price": Product.price,
        "created_at": Product.created_at,
        "id": Product.id,
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        Product.created_at,
    )

    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # -----------------------------------------
    # Pagination
    # -----------------------------------------

    query = query.offset(skip).limit(limit)

    # -----------------------------------------
    # Execute product query
    # -----------------------------------------

    result = await session.execute(query)

    products = result.scalars().unique().all()

    # -----------------------------------------
    # Return paginated response
    # -----------------------------------------

    return PaginatedResponse(
        items=products,
        total=total,
        skip=skip,
        limit=limit,
        page=page,
        total_pages=total_pages,
    )


async def read_product(
    product_id: str,
    session: AsyncSession,
) -> Product:
    return await get_product_by_id(
        product_id=product_id,
        session=session,
    )


async def delete_product(
    product_id: str,
    session: AsyncSession,
) -> dict:
    product = await get_product_by_id(
        product_id=product_id,
        session=session,
    )

    try:
        await session.delete(product)
        await session.commit()

    except Exception:
        await session.rollback()
        raise

    return {
        "status": 200,
        "message": "Product deleted successfully",
    }


async def create_order_with_images():
    pass
