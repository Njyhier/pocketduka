from app.schemas.role_schemas import RoleCreate
from app.schemas.Baseschema import DeleteResponce
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.roles import Role
from fastapi import HTTPException, status


async def get_role_by_id(role_id: str, session: AsyncSession) -> Role:
    result = await session.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist"
        )
    return role


async def create_role(role_data: RoleCreate, session: AsyncSession) -> Role:
    role = Role(**role_data.model_dump())
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def read_roles(session: AsyncSession) -> list[Role]:
    result = await session.execute(select(Role))
    roles = result.scalars().all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No roles were found"
        )
    return roles


async def read_role(role_id: str, session: AsyncSession) -> Role:
    role = await get_role_by_id(role_id, session)
    return role


async def update_role(role_id: str, update_data: RoleCreate, session: AsyncSession) -> Role:
    role_to_update = await get_role_by_id(role_id, session)
    update_data = update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role_to_update, key, value)
    await session.commit()
    await session.refresh(role_to_update)
    return role_to_update


async def delete_role(role_id: str, session: AsyncSession) -> DeleteResponce:
    role_to_delete = await get_role_by_id(role_id, session)
    await session.delete(role_to_delete)
    await session.commit()
    return {"message": "Role dleted successfuly"}
