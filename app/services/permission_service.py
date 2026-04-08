from app.schemas.permission_schemas import PermissionCreate, PermissionUpdate
from app.schemas.Baseschema import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permissions import Permission
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def get_permission_by_id(permission_id: str, session: AsyncSession) -> Permission:
    result = await session.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission does not exist"
        )
    return permission


async def get_permission_by_name(
    permission_name: str, session: AsyncSession
) -> Permission:
    print("GETTING PERMISSION BY NAME")
    result = await session.execute(
        select(Permission)
        .where(Permission.name == permission_name)
        .options(selectinload(Permission.roles))
    )
    permission = result.scalar_one_or_none()
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission does not exist"
        )
    return permission


async def create_permission(
    permission_data: PermissionCreate, session: AsyncSession
) -> Permission:
    permission = Permission(**permission_data.model_dump())
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


async def read_permissions(
    session: AsyncSession,
    skip: int,
    limit: int,
) -> list[Permission]:
    result = await session.execute(
        select(Permission).offset(skip).limit(limit),
    )
    permissions = result.scalars().all()
    if not permissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No permissions were found"
        )
    return permissions


async def read_permission(permission_id: str, session: AsyncSession) -> Permission:
    permission = await get_permission_by_id(permission_id, session)
    return permission


async def update_permission(
    permission_id: str, update_data: PermissionUpdate, session: AsyncSession
) -> Permission:
    permission_to_update = await get_permission_by_id(permission_id, session)
    update_data = update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(permission_to_update, key, value)
    await session.commit()
    await session.refresh(permission_to_update)
    return permission_to_update


async def delete_permission(permission_id: str, session: AsyncSession) -> ApiResponse:
    permission_to_delete = await get_permission_by_id(permission_id, session)
    await session.delete(permission_to_delete)
    await session.commit()
    return {"message": "Permission dleted successfuly"}


async def read_permissions_by_ids(
    ids: list[str],
    session: AsyncSession,
) -> list[Permission]:
    result = await session.execute(select(Permission).where(Permission.id.in_(ids)))
    return list(result.scalars().all())
