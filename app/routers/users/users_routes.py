from app.schemas.role_schemas import UserRoleUpdate
from app.schemas.Baseschema import ApiResponse
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
from app.services.auth_service import (
    require_roles_dep,
    get_current_user,
    get_user_roles,
)
from app.models.user import User
from app.services.auth_service import login_for_access_token
from app.middlewares.rbac_middleware import SystemTasks

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


@router.post("/sign_up", response_model=ApiResponse[UserReadPrivate])
async def sign_up(
    user_data: UserSignUp,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_user(session, user_data)
    return {
        "status": 201,
        "message": "Signup Successful",
        "payload": payload,
    }


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):

    return await login_for_access_token(form_data, session)


@router.post("/users", response_model=ApiResponse[UserReadPrivate])
@SystemTasks("create_users")
async def create_user_route(
    user_data: UserWrite,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_user(session, user_data)
    return {
        "status": 201,
        "message": "User created successfully",
        "payload": payload,
    }


@router.get("/users", response_model=ApiResponse[list[UserReadPrivate]])
@SystemTasks("read_users")
async def read_users_route(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    payload = await read_users(session, skip, limit)
    return {
        "status": 200,
        "message": "Users retrieved",
        "payload": payload,
    }


@router.get("/users/by_email", response_model=ApiResponse[UserReadPrivate])
@SystemTasks("read_users")
async def read_user_by_email(
    email: str, session: AsyncSession = Depends(get_async_session)
):
    payload = await get_user_by_email(email, session)
    return {
        "status": 200,
        "message": "User retrieved",
        "payload": payload,
    }


@router.get("/users/by_username", response_model=ApiResponse[UserReadPrivate])
@SystemTasks("read_users")
async def get_user_by_username_route(
    username: str, session: AsyncSession = Depends(get_async_session)
):
    payload = await get_user_by_username(username, session)
    return {
        "status": 200,
        "message": "User retrieved",
        "payload": payload,
    }


@router.get("/users/{user_id}", response_model=ApiResponse[UserReadPrivate])
@SystemTasks("read_users")
async def read_user_route(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):

    payload = await get_user_by_user_id(user_id, session)
    return {
        "status": 200,
        "message": "User retrieved",
        "payload": payload,
    }


@router.put("/users/{user_id}", response_model=ApiResponse[UserReadPrivate])
@SystemTasks("update_users")
async def update_user_route(
    user_data: UserUpdate,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await update_user(user_data, user_id, session)
    return {
        "status": 200,
        "message": "User Updated",
        "payload": payload,
    }


@router.delete("/users/{user_id}")
@SystemTasks("delete-users")
async def delete_user_route(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_user(user_id, session)


@router.patch("/users/{user_id}/roles")
@SystemTasks("update_users")
async def update_user_roles_route(
    user_id: str,
    role_update: UserRoleUpdate,
    session: AsyncSession = Depends(get_async_session),
):

    return await update_user_roles(user_id, role_update, session)


@router.patch("/users/me")
async def edit_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_id = current_user.id
    return await update_user(user_data, user_id, session)


@router.get("/user/roles", response_model=ApiResponse[list[str]])
@SystemTasks("read_user_roles")
async def get_roles_route(
    user=Depends(get_current_user),
):
    payload = await get_user_roles(
        user=user,
    )

    return {
        "status": 200,
        "message": "Roles retrieved",
        "payload": payload,
    }
