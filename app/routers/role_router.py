from fastapi import APIRouter, Depends
from app.schemas.Baseschema import DeleteResponce
from app.schemas.role_schemas import BaseRole, RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.role_service import (
    create_role,
    read_role,
    read_roles,
    delete_role,
    update_role,
)

router = APIRouter()


@router.post("/roles", response_model=BaseRole)
async def create_role_route(
    role_data: RoleCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_role(role_data, session)


@router.get("/roles", response_model=list[BaseRole])
async def read_roles_route(
    session: AsyncSession = Depends(get_async_session),
):
    return await read_roles(session)


@router.get("/roles/{role_id}", response_model=BaseRole)
async def read_role_route(
    role_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await read_role(role_id, session)


@router.put("/roles/{role_id}", response_model=BaseRole)
async def update_role_route(
    role_data: RoleCreate,
    role_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_role(role_id, role_data, session)


@router.delete("/roles/{role_id}", response_model=DeleteResponce)
async def delete_role_route(
    role_id: str, session: AsyncSession = Depends(get_async_session)
):
    return await delete_role(role_id, session)
