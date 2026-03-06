from app.schemas.user_schemas import (
    UserWrite,
    UserUpdate,
    DeleteResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.user import User
from sqlalchemy import select, String
from uuid import UUID


async def create_user(session: AsyncSession, user_create: UserWrite) -> User:
    res = await session.execute(select(User).where(User.email == user_create.email))
    user = res.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    hashed_pwd = "password"
    db_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        username=user_create.username,
        password_hash=hashed_pwd,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def read_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users were found"
        )
    return users


async def read_user(session: AsyncSession, user_id: str) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def read_user_me(user: User) -> User:
    return user


async def update_user(
    user_update: UserUpdate, user_id: str, session: AsyncSession
) -> User:

    result = await session.execute(select(User).where(User.id == user_id))
    user_to_update = result.scalar_one_or_none()
    if user_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
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
) -> DeleteResponse:
    result = await session.execute(select(User).where(User.id == user_id))
    user_to_delete = result.scalar_one_or_none()
    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await session.delete(user_to_delete)
    await session.commit()
    await session.refresh()
    return {"message": "User deleted successfuly"}
