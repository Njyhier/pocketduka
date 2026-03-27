from fastapi import APIRouter, Depends, Query
from app.schemas.Baseschema import DeleteResponce
from app.schemas.role_schemas import BaseRole, RoleCreate, RoleRead, RoleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.role_service import (
    create_role,
    get_role_by_name,
    read_roles,
    delete_role,
    update_role,
)
from app.services.auth_service import require_roles_dep

router = APIRouter()


@router.post("/roles", response_model=RoleRead)
async def create_role_route(
    role_data: RoleCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_role(role_data, session)


@router.get("/roles", response_model=list[RoleRead])
async def read_roles_route(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    return await read_roles(
        session,
        skip=skip,
        limit=limit,
    )


@router.get("/roles/name", response_model=RoleRead)
async def read_role_by_name_route(
    role_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_role_by_name(role_name, session)


@router.put("/roles/name", response_model=RoleRead)
async def update_role_permissions(
    role_data: RoleUpdate,
    role_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_role(role_name, role_data, session)


@router.delete("/roles/name", response_model=DeleteResponce)
async def delete_role_route(
    role_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_role(role_name, session)
