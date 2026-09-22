from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session

from app.schemas.user_schemas import (
    UserWrite,
    UserUpdate,
    UserReadPrivate,
)

from app.schemas.Baseschema import PaginatedResponse

from app.schemas.role_schemas import UserRoleUpdate

from app.services.user_service import (
    create_user,
    read_users,
    get_user,
    update_user,
    delete_user,
    update_user_roles,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


SessionDep = Annotated[
    AsyncSession,
    Depends(get_async_session),
]


@router.post(
    "",
    response_model=UserReadPrivate,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user_create: UserWrite,
    session: SessionDep,
):
    return await create_user(
        session=session,
        user_create=user_create,
    )


@router.get(
    "",
    response_model=PaginatedResponse[UserReadPrivate],
)
async def read_users_endpoint(
    session: SessionDep,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
    ),
):
    return await read_users(
        session=session,
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get(
    "/{user_id}",
    response_model=UserReadPrivate,
)
async def get_user_endpoint(
    user_id: str,
    session: SessionDep,
):
    return await get_user(
        user_id=user_id,
        session=session,
    )


@router.patch(
    "/{user_id}",
    response_model=UserReadPrivate,
)
async def update_user_endpoint(
    user_id: str,
    user_update: UserUpdate,
    session: SessionDep,
):
    return await update_user(
        user_id=user_id,
        user_update=user_update,
        session=session,
    )


@router.patch(
    "/{user_id}/roles",
    response_model=UserReadPrivate,
)
async def update_user_roles_endpoint(
    user_id: str,
    update_data: UserRoleUpdate,
    session: SessionDep,
):
    return await update_user_roles(
        user_id=user_id,
        update_data=update_data,
        session=session,
    )


@router.delete(
    "/{user_id}",
)
async def delete_user_endpoint(
    user_id: str,
    session: SessionDep,
):
    return await delete_user(
        user_id=user_id,
        session=session,
    )
