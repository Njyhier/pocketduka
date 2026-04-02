from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schemas.Baseschema import ApiResponse
from app.schemas.cart_schema import CartRead

from app.models.user import User


from app.services.auth_service import get_current_user

from app.services.cart_service import (
    create_cart,
    clear_cart_items,
    get_cart_by_user_id,
    read_carts,
)

router = APIRouter()


@router.post("/carts")
async def create_cart_route(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await create_cart(user_id=user.id, session=session)


@router.patch("/carts/{cartId}")
async def clear_cart_items_route(
    cart_id: str, session: AsyncSession = Depends(get_async_session)
):
    return await clear_cart_items(cart_id=cart_id, session=session)


@router.get("/carts")
async def read_carts_route(session: AsyncSession = Depends(get_async_session)):
    return await read_carts(session=session)


@router.get("/carts/by_user_id", response_model=ApiResponse[CartRead])
async def get_cart_by_uid(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    payload = await get_cart_by_user_id(
        user_id=user.id,
        session=session,
    )
    return {
        "status": 200,
        "message": "Cart retrieved successfuly",
        "payload": payload,
    }
