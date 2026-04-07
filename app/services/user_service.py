from app.schemas.user_schemas import (
    UserWrite,
    UserUpdate,
)
from app.schemas.role_schemas import UserRoleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.user import User
from sqlalchemy import select, or_
from app.utils.password import get_password_hash
from app.utils.user_utils import get_user_by_user_id
from .role_service import get_role_by_name
from app.services.cart_service import create_cart


async def create_user(session: AsyncSession, user_create: UserWrite):
    res = await session.execute(
        select(User).where(
            or_(
                User.email == user_create.email,
                User.username == user_create.username,
            )
        )
    )
    user = res.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    db_user = User(
        email=user_create.email,
        username=user_create.username,
        password_hash=await get_password_hash(user_create.password),
    )
    session.add(db_user)
    await session.flush()
    await create_cart(user_id=db_user.id, session=session)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def read_users(
    session: AsyncSession,
    skip: int,
    limit: int,
):
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


async def update_user(
    user_update: UserUpdate,
    user_id: str,
    session: AsyncSession,
):
    user_to_update = await get_user_by_user_id(user_id, session)
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_to_update, key, value)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(user_to_update)
    return user_to_update


async def delete_user(
    user_id: str,
    session: AsyncSession,
):
    result = await session.execute(select(User).where(User.id == user_id))
    user_to_delete = result.scalar_one_or_none()
    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await session.delete(user_to_delete)
    await session.commit()
    return {"message": "User deleted successfuly"}


async def update_user_roles(
    user_id: str, update_data: UserRoleUpdate, session: AsyncSession
):
    user_to_upgrade = await get_user_by_user_id(user_id, session=session)
    roles = user_to_upgrade.roles
    existing_roles = {role.id for role in roles}

    for name in update_data.role_names:
        role = await get_role_by_name(name, session)
        if role not in roles:
            roles.append(role)
            existing_roles.add(role.id)
    await session.commit()
    await session.refresh(user_to_upgrade)
    return user_to_upgrade
