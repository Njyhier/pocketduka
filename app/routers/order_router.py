from fastapi import APIRouter, Depends
from app.schemas.Baseschema import ApiResponse
from app.schemas.order_schema import OrderRead
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import get_current_user
from app.db.session import get_async_session
from app.services.order_service import (
    create_order_with_items,
    update_order_status,
    read_orders_by_cart_id,
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
