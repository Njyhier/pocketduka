from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user


async def get_user_by_id(user_id: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user
