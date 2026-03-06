from app.schemas.user_schemas import (
    UserReadPrivate,
    UserWrite,
    UserReadPublic,
    UserUpdate,
    DeleteResponse,
)
from app.services.user.user_service import (
    read_users,
    create_user,
    read_user,
    read_user_me,
    update_user,
    delete_user,
)
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from uuid import UUID

router = APIRouter()


@router.post("/users")
async def create_user_route(
    user_data: UserWrite,
    session: AsyncSession = Depends(get_async_session),
) -> UserReadPublic:
    return await create_user(session, user_data)


@router.get("/users", response_model=list[UserReadPrivate])
async def read_users_route(
    session: AsyncSession = Depends(get_async_session),
) -> list[UserReadPublic]:
    return await read_users(session)


@router.get("/users/{user_id}", response_model=UserReadPrivate)
async def read_user_route(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await read_user(session, user_id)


@router.put("/users/{user_id}", response_model=UserReadPublic)
async def update_user_route(
    user_data: UserUpdate,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_user(user_data, user_id, session)


@router.delete("/users/{user_id}", response_model=DeleteResponse)
async def delete_user_route(
    user_id: str, session: AsyncSession = Depends(get_async_session)
):
    return await delete_user(user_id, session)
