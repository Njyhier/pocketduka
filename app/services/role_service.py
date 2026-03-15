from app.schemas.role_schemas import RoleCreate, RoleUpdate
from app.schemas.Baseschema import DeleteResponce
from app.models import user
from app.services.auth_service import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.roles import Role
from fastapi import HTTPException, status, Depends
from app.services.permission_service import read_permissions_by_ids
import asyncio


async def get_role_by_name(role_name: str, session: AsyncSession) -> Role:
    result = await session.execute(select(Role).where(Role.name == role_name))
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist"
        )
    return role


async def create_role(role_data: RoleCreate, session: AsyncSession) -> Role:
    role_dict = role_data.model_dump()
    permissions = await read_permissions_by_ids(role_data.permissions, session=session)
    role_dict["permissions"] = permissions
    role = Role(**role_dict)
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def read_roles(session: AsyncSession) -> list[Role]:
    result = await session.execute(select(Role).options(selectinload(Role.permissions)))
    roles = result.scalars().all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No roles were found"
        )
    return roles


async def read_role(role_name: str, session: AsyncSession) -> Role:
    role = await get_role_by_name(role_name, session)
    return role


async def update_role(
    role_name: str, update_data: RoleUpdate, session: AsyncSession
) -> Role:
    role_to_update = await get_role_by_name(role_name, session)
    update_data = update_data.model_dump(exclude_unset=True)
    if "permissions" in update_data:
        permissions = await read_permissions_by_ids(*update_data.pop("permissions"))
        for perm in permissions:
            if perm not in role_to_update.permissions and perm is not None:
                role_to_update.permissions.append(perm)

    for key, value in update_data.items():
        setattr(role_to_update, key, value)

    await session.commit()
    await session.refresh(role_to_update)
    return role_to_update


async def delete_role(role_name: str, session: AsyncSession) -> DeleteResponce:
    role_to_delete = await get_role_by_name(role_name, session)
    await session.delete(role_to_delete)
    await session.commit()
    return {"message": "Role dleted successfuly"}


async def read_roles_by_names(*role_names: str, session: AsyncSession) -> list[Role]:
    caroutines = [get_role_by_name(role_name, session) for role_name in role_names]
    result = await asyncio.gather(*caroutines)
    return result
