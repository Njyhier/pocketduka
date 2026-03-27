from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_async_session
from app.models.user import User
from app.models.cart import Cart

from app.services.auth_service import get_current_user
from app.services.catrItem_service import (
    create_cart_item,
    decrement_item_quantity,
    increment_item_quantity,
    add_item_to_cart,
)

router = APIRouter()


@router.post("/cartitems")
async def create_cart_item_route(
    product_id: str,
    cart_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_cart_item(
        product_id=product_id,
        cart_id=cart_id,
        session=session,
    )


@router.patch("/cartitems/")
async def add_item_to_cart_route(
    product_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):

    res = await session.execute(select(Cart).where(Cart.user_id == user.id))
    cart = res.scalar_one_or_none()
    return await add_item_to_cart(
        product_id=product_id,
        cart_id=cart.id,
        session=session,
    )


@router.patch("/cartitems/increment_quantity/{item_id}")
async def increment_item_quantity_route(
    item_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await increment_item_quantity(item_id=item_id, session=session)


@router.patch("/cartitems/decrement_quantity/{item_id}")
async def decrement_item_quantity_route(
    item_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await decrement_item_quantity(item_id=item_id, session=session)
