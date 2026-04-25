from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select
from app.models.order import Order

from app.services.cart_service import get_cart_by_user_id
from app.services.order_item_service import create_order_item
from app.services.cart_service import clear_cart_items
from app.services.payment_service import create_payment


async def create_order_with_items(user_id: str, payment_id: str, session: AsyncSession):
    cart = await get_cart_by_user_id(user_id=user_id, session=session)

    cart_id = cart.id
    db_order = Order(
        cart_id=cart_id,
        total_amount=cart.subtotal,
        payment_id=payment_id,
    )
    session.add(db_order)
    await session.flush()
    order_items = []
    for item in cart.items:
        order_item = await create_order_item(
            order_id=db_order.id,
            cart_item=item,
            session=session,
        )
        order_items.append(order_item)
    await clear_cart_items(cart_id=cart_id, session=session)

    return {
        "order": db_order,
        "order_items": order_items,
    }


async def get_order_by_id(order_id: str, session: AsyncSession):
    res = await session.execute(select(Order).where(Order.id == order_id))
    order = res.scalar_one_or_none()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


async def update_order_status(order_id: str, session: AsyncSession):
    order = await get_order_by_id(order_id=order_id, session=session)
    order.update_status()
    await session.commit()
    await session.refresh(order)
    return {
        "status": 200,
        "message": "Order status updated successfully",
        "payload": order.status,
    }


async def read_orders_by_cart_id(cart_id: str, session: AsyncSession):
    result = await session.execute(select(Order).where(Order.cart_id == cart_id))
    orders = result.scalars().all()
    return orders


async def get_all_orders(session: AsyncSession):
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return orders
