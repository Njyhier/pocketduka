from app.schemas.role_schemas import UserRoleUpdate
from app.schemas.Baseschema import DeleteResponce
from app.utils.user_utils import (
    get_user_by_username,
    get_user_by_email,
    get_user_by_user_id,
)
from fastapi import Depends, APIRouter, Query
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token_schemas import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import require_roles_dep, get_current_user
from app.services.auth_service import login_for_access_token

from app.schemas.user_schemas import (
    UserReadPrivate,
    UserWrite,
    UserUpdate,
    UserSignUp,
)
from app.services.user_service import (
    read_users,
    create_user,
    update_user,
    delete_user,
    update_user_roles,
)


router = APIRouter()


@router.post("/sign_up")
async def sign_up(
    user_data: UserSignUp,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_user(session, user_data)


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):

    return await login_for_access_token(form_data, session)


@router.post("/users", response_model=UserReadPrivate)
async def create_user_route(
    user_data: UserWrite,
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin")),
):
    return await create_user(session, user_data)


@router.get("/users", response_model=list[UserReadPrivate])
async def read_users_route(
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin", "owner")),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
) -> list[UserReadPrivate]:
    return await read_users(session, skip, limit)


@router.get("/users/by_email", response_model=UserReadPrivate)
async def read_user_by_email(
    email: str, session: AsyncSession = Depends(get_async_session)
):
    return await get_user_by_email(email, session)


@router.get("/users/by_username", response_model=UserReadPrivate)
async def get_user_by_username_route(
    username: str, session: AsyncSession = Depends(get_async_session)
):
    user = await get_user_by_username(username, session)
    return user


@router.get("/users/{user_id}", response_model=UserReadPrivate)
async def read_user_route(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):

    user = await get_user_by_user_id(user_id, session)
    return user


@router.put("/users/{user_id}", response_model=UserReadPrivate)
async def update_user_route(
    user_data: UserUpdate,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin", "owner")),
):
    return await update_user(user_data, user_id, session)


@router.delete("/users/{user_id}", response_model=DeleteResponce)
async def delete_user_route(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin", "owner")),
):
    return await delete_user(user_id, session)


@router.patch("/users/{user_id}/roles", response_model=UserReadPrivate)
async def update_user_roles_route(
    user_id: str,
    role_update: UserRoleUpdate,
    session: AsyncSession = Depends(get_async_session),
    _: bool = Depends(require_roles_dep("admin", "owner")),
):

    return await update_user_roles(user_id, role_update, session)


@router.patch("/users/me", response_model=UserReadPrivate)
async def edit_profile(
    user_data: UserUpdate,
    current_user: UserReadPrivate = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_id = current_user.id
    return await update_user(user_data, user_id, session)
