from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.user import User
from fastapi import HTTPException, status

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
)


async def get_user_by_username(username: str, session: AsyncSession):
    username = username.strip()
    result = await session.execute(
        select(User)
        .where(User.username == username)
        .options(
            selectinload(User.roles),
            selectinload(User.cart),
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise user_not_found_exception
    return user


async def get_user_by_email(email: str, session: AsyncSession):
    email = email.strip().lower()
    result = await session.execute(select(User).where(func.lower(User.email) == email))
    user = result.scalar_one_or_none()
    if not user:
        raise user_not_found_exception
    return user


async def get_user_by_user_id(user_id: str, session: AsyncSession):
    user_id = user_id.strip()
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.roles),
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    return user
