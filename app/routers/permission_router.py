from fastapi import APIRouter, Depends
from app.schemas.Baseschema import DeleteResponce
from app.schemas.permission_schemas import PermissionCreate, PermissionRead,PermissionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.permission_service import (
    create_permission,
    read_permissions,
    read_permission,
    delete_permission,
    update_permission,
)

router = APIRouter()

@router.post("/permissions", response_model=PermissionRead)
async def create_permission_route(
    permission_data: PermissionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_permission(permission_data, session)


@router.get("/permissions", response_model=list[PermissionRead])
async def read_permissions_route(
    session: AsyncSession = Depends(get_async_session),
):
    return await read_permissions(session)

@router.get("/permissions/{permission_id}", response_model=PermissionRead)
async def read_permission_route(
    permission_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await read_permission(permission_id, session)


@router.put("/permissions/{permission_id}", response_model=PermissionRead)
async def update_permission_route(
    permission_data: PermissionUpdate,
    permission_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_permission(permission_id, permission_data, session)


@router.delete("/permissions/{permission_id}", response_model=DeleteResponce)
async def delete_permission_route(
    permission_id: str, session: AsyncSession = Depends(get_async_session)
):
    return await delete_permission(permission_id, session)