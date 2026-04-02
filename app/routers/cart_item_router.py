from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_async_session
from app.models.user import User
from app.models.cart import Cart
from app.schemas.cart_item_schema import CartItemRead

from app.services.auth_service import get_current_user
from app.schemas.Baseschema import ApiResponse
from app.services.cartItem_service import (
    create_cart_item,
    decrement_item_quantity,
    increment_item_quantity,
    add_item_to_cart,
    read_cart_items,
)


router = APIRouter()


@router.post("/cartitems/{product_id}")
async def create_cart_item_route(
    product_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_cart_item(
        product_id=product_id,
        cart_id=user.cart.id,
        session=session,
    )
    return {
        "status": 201,
        "message": "Item  created successfuly",
        "payload": payload,
    }


@router.patch("/cartitems")
async def add_item_to_cart_route(
    product_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):

    res = await session.execute(select(Cart).where(Cart.user_id == user.id))
    cart = res.scalar_one_or_none()
    payload = await add_item_to_cart(
        product_id=product_id,
        cart_id=cart.id,
        session=session,
    )
    return {
        "status": 200,
        "message": "Item added to cart successfully",
        "payload": payload,
    }


@router.patch("/cartitems/increment_quantity/{item_id}")
async def increment_item_quantity_route(
    item_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await increment_item_quantity(item_id=item_id, session=session)
    return {
        "status": 200,
        "message": " Increment successful",
        "payload": payload,
    }


@router.patch("/cartitems/decrement_quantity/{item_id}")
async def decrement_item_quantity_route(
    item_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await decrement_item_quantity(item_id=item_id, session=session)
    return {
        "status": 200,
        "message": "Decrement successful",
        "payload": payload,
    }


@router.get("/cartitems", response_model=ApiResponse[list[CartItemRead]])
async def read_cart_items_route(
    cart_id: str, session: AsyncSession = Depends(get_async_session)
):
    payload = await read_cart_items(
        cart_id=cart_id,
        session=session,
    )
    return {
        "status": 200,
        "message": "Items retrieval successful",
        "payload": payload,
    }
