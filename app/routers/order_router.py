from fastapi import APIRouter, Depends
from app.schemas.Baseschema import ApiResponse
from app.schemas.order_schema import OrderRead
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import get_current_user, require_roles_dep
from app.db.session import get_async_session
from app.middlewares.rbac_middleware import SystemTasks
from app.services.order_service import (
    create_order_with_items,
    update_order_status,
    read_orders_by_cart_id,
    get_all_orders,
)

router = APIRouter()


@router.post("/orders")
async def place_order(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    payload = await create_order_with_items(user_id=user.id, session=session)
    return {
        "status": 201,
        "message": "Order placed successfully",
        "payload": payload,
    }


@router.patch("/orders/{order_id}")
@SystemTasks("update_orders")
async def update_order_status_route(
    order_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_order_status(
        order_id=order_id,
        session=session,
    )


@router.get("/orders/cart_id", response_model=ApiResponse[list[OrderRead]])
async def read_cart_orders(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    payload = await read_orders_by_cart_id(
        cart_id=user.cart.id,
        session=session,
    )
    return {
        "status": 201,
        "message": "Orders retrieved successfully",
        "payload": payload,
    }


@router.get("/orders")
@SystemTasks("read_all_orders")
async def get_all_orders_route(
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin", "owner")),
):
    payload = await get_all_orders(session=session)
    return {
        "status": 201,
        "message": "Orders retrieved successfully",
        "payload": payload,
    }
