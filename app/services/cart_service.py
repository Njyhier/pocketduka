from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, select, delete
from fastapi import HTTPException, status
from app.models.cart import Cart
from app.models.cart_item import CartItem


async def get_cart_by_user_id(user_id: str, session: AsyncSession):
    res = await session.execute(
        select(Cart).where(Cart.user_id == user_id).options(selectinload(Cart.items))
    )
    cart = res.scalar_one_or_none()
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    return cart


async def get_cart_by_id(cart_id: str, session: AsyncSession):
    result = await session.execute(
        select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart_id)
    )
    cart = result.scalar_one_or_none()
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found",
        )
    return cart


async def create_cart(user_id: str, session: AsyncSession):
    res = await session.execute(select(Cart).where(Cart.user_id == user_id))
    cart = res.scalar_one_or_none()
    if cart is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a cart",
        )
    db_cart = Cart(user_id=user_id)
    session.add(db_cart)
    # await session.commit()
    # await session.refresh(db_cart)
    return db_cart


async def clear_cart_items(cart_id: str, session: AsyncSession):
    await session.execute(
        delete(CartItem)
        .where(CartItem.cart_id == cart_id)
        .execution_options(synchronize_session=False),
    )
    return {
        "status": 200,
        "message": "Items cleared successfully",
    }


async def read_carts(session: AsyncSession):
    result = await session.execute(select(Cart))
    carts = result.scalars().all()
    return carts
