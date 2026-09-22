from app.schemas.role_schemas import RoleCreate, RoleUpdate
from app.schemas.Baseschema import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.roles import Role
from fastapi import HTTPException, status
from app.services.permission_service import (
    read_permissions_by_ids,
    get_permission_by_name,
)
import asyncio


async def get_role_by_name(role_name: str, session: AsyncSession) -> Role:
    result = await session.execute(
        select(Role)
        .where(Role.name == role_name)
        .options(selectinload(Role.permissions))
    )
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist"
        )
    return role


async def create_role(
    role_create: RoleCreate,
    session: AsyncSession,
):
    role = Role(
        name=role_create.name,
    )

    session.add(role)

    await session.commit()

    result = await session.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role.id)
    )

    role = result.scalar_one()

    return role


async def read_roles(
    session: AsyncSession,
    skip: int,
    limit: int,
) -> list[Role]:
    result = await session.execute(
        select(Role).offset(skip).limit(limit).options(selectinload(Role.permissions))
    )
    roles = result.scalars().all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No roles were found"
        )
    return roles


# async def read_role(role_name: str, session: AsyncSession) -> Role:
#     role = await get_role_by_name(role_name, session)
#     return role


async def update_role(
    role_name: str, update_data: RoleUpdate, session: AsyncSession
) -> Role:
    role_to_update = await get_role_by_name(role_name, session)
    update_data = update_data.model_dump(exclude_unset=True)
    if "permissions" in update_data:
        permission_names = update_data.pop("permissions")
        for name in permission_names:
            perm = await get_permission_by_name(name, session=session)
            if perm not in role_to_update.permissions:
                role_to_update.permissions.append(perm)
        await session.commit()
    await session.refresh(role_to_update)
    return role_to_update


async def delete_role(role_name: str, session: AsyncSession) -> ApiResponse:
    role_to_delete = await get_role_by_name(role_name, session)
    await session.delete(role_to_delete)
    await session.commit()
    return {"status": True, "payload": {"message": "Role deleted successfully"}}


# async def read_roles_by_names(*role_names: str, session: AsyncSession) -> list[Role]:
#     caroutines = [get_role_by_name(role_name, session) for role_name in role_names]
#     result = await asyncio.gather(*caroutines)
#     return result
