from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from app.services import cart_service, product_service
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.schemas.order_item_schema import OrderItemCreate

from app.models.user import User
from app.models.cart import Cart


async def get_item_by_id(item_id: str, session: AsyncSession) -> CartItem:
    result = await session.execute(select(OrderItem).where(OrderItem.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


async def create_order_item(
    order_id: str,
    cart_item: CartItem,
    session: AsyncSession,
) -> OrderItem:
    res = cart_item
    item = OrderItem(
        id=res.id,
        product_id=res.product_id,
        quantity=res.quantity,
        price=res.price,
        image_url=res.image_url,
        order_id=order_id,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
