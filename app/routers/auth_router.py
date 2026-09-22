from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.user import User
from app.schemas.token_schemas import Token
from app.schemas.user_schemas import UserReadPrivate

from app.services.auth_service import (
    login_for_access_token,
    get_current_user,
    get_current_user_roles,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# LOGIN
# ============================================================


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: AsyncSession = Depends(get_async_session),
) -> Token:

    return await login_for_access_token(
        form_data,
        session,
    )


# ============================================================
# CURRENT USER
# ============================================================


@router.get(
    "/me",
    response_model=UserReadPrivate,
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:

    return current_user


# ============================================================
# CURRENT USER ROLES
# ============================================================


@router.get(
    "/me/roles",
    response_model=list[str],
)
async def get_my_roles(
    current_user: User = Depends(get_current_user),
) -> list[str]:

    return await get_current_user_roles(current_user)
