# from app.schemas.user_schemas import (
#     UserWrite,
#     UserUpdate,
# )
# from app.schemas.role_schemas import UserRoleUpdate
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import HTTPException, status
# from app.models.user import User
# from sqlalchemy import select, or_
# from app.utils.password import get_password_hash
# from app.utils.user_utils import get_user_by_user_id
# from .role_service import get_role_by_name
# from app.services.cart_service import create_cart


# async def create_user(session: AsyncSession, user_create: UserWrite):
#     res = await session.execute(
#         select(User).where(
#             or_(
#                 User.email == user_create.email,
#                 User.username == user_create.username,
#             )
#         )
#     )
#     user = res.scalar_one_or_none()
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User already exists",
#         )
#     db_user = User(
#         email=user_create.email,
#         username=user_create.username,
#         password_hash=await get_password_hash(user_create.password),
#     )
#     session.add(db_user)
#     await session.flush()
#     await create_cart(user_id=db_user.id, session=session)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user


# async def read_users(
#     session: AsyncSession,
#     skip: int,
#     limit: int,
# ):
#     result = await session.execute(select(User).offset(skip).limit(limit))
#     users = result.scalars().all()
#     return users


# async def update_user(
#     user_update: UserUpdate,
#     user_id: str,
#     session: AsyncSession,
# ):
#     user_to_update = await get_user_by_user_id(user_id, session)
#     update_data = user_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(user_to_update, key, value)
#     try:
#         await session.commit()
#     except Exception:
#         await session.rollback()
#         raise

#     await session.refresh(user_to_update)
#     return user_to_update


# async def delete_user(
#     user_id: str,
#     session: AsyncSession,
# ):
#     result = await session.execute(select(User).where(User.id == user_id))
#     user_to_delete = result.scalar_one_or_none()
#     if user_to_delete is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )
#     await session.delete(user_to_delete)
#     await session.commit()
#     return {"message": "User deleted successfuly"}


# async def update_user_roles(
#     user_id: str, update_data: UserRoleUpdate, session: AsyncSession
# ):
#     user_to_upgrade = await get_user_by_user_id(user_id, session=session)
#     roles = user_to_upgrade.roles
#     existing_roles = {role.id for role in roles}

#     for name in update_data.role_names:
#         role = await get_role_by_name(name, session)
#         if role not in roles:
#             roles.append(role)
#             existing_roles.add(role.id)
#     await session.commit()
#     await session.refresh(user_to_upgrade)
#     return user_to_upgrade


from app.schemas.user_schemas import (
    UserWrite,
    UserUpdate,
)
from app.schemas.role_schemas import UserRoleUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.models.user import User
from app.models.roles import Role


from app.utils.password import get_password_hash
from app.utils.user_utils import get_user_by_user_id, get_user_by_username

from .role_service import get_role_by_name
from sqlalchemy import func
from sqlalchemy.orm import selectinload


async def create_user(
    session: AsyncSession,
    user_create: UserWrite,
) -> User:

    # --------------------------------------------------
    # 1. Check whether username already exists
    # --------------------------------------------------

    existing_user = await get_user_by_username(
        username=user_create.username,
        session=session,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    # --------------------------------------------------
    # 2. Get default customer role
    # --------------------------------------------------

    result = await session.execute(select(Role).where(Role.name == "customer"))

    customer_role = result.scalar_one_or_none()

    if customer_role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default customer role does not exist",
        )

    # --------------------------------------------------
    # 3. Create user with customer role
    # --------------------------------------------------

    user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=await get_password_hash(user_create.password),
        roles=[customer_role],
    )

    session.add(user)

    # --------------------------------------------------
    # 4. Save user + relationship
    # --------------------------------------------------

    await session.commit()

    # --------------------------------------------------
    # 5. Reload with roles eagerly loaded
    # --------------------------------------------------

    result = await session.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user.id)
    )

    user = result.scalar_one()

    return user


async def read_users(
    session: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than or equal to 1",
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 100",
        )

    # -----------------------------------
    # Base query
    # -----------------------------------

    query = select(User).options(selectinload(User.roles))

    # -----------------------------------
    # Search
    # -----------------------------------

    if search:
        search_pattern = f"%{search}%"

        query = query.where(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern),
            )
        )

    # -----------------------------------
    # Count
    # -----------------------------------

    count_query = select(func.count(User.id))

    if search:
        count_query = count_query.where(
            or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern),
            )
        )

    count_result = await session.execute(count_query)

    total = count_result.scalar_one()

    # -----------------------------------
    # Pagination
    # -----------------------------------

    offset = (page - 1) * page_size

    query = query.offset(offset).limit(page_size)

    result = await session.execute(query)

    users = result.scalars().all()

    # -----------------------------------
    # Pagination metadata
    # -----------------------------------

    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return {
        "items": users,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


async def get_user(
    user_id: str,
    session: AsyncSession,
):
    """
    Retrieve a single user by ID.
    """

    return await get_user_by_user_id(
        user_id=user_id,
        session=session,
    )


async def update_user(
    user_update: UserUpdate,
    user_id: str,
    session: AsyncSession,
):
    user_to_update = await get_user_by_user_id(
        user_id=user_id,
        session=session,
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
):
    user_to_delete = await get_user_by_user_id(
        user_id=user_id,
        session=session,
    )

    await session.delete(user_to_delete)

    await session.commit()

    return {"message": "User deleted successfully"}


async def update_user_roles(
    user_id: str,
    update_data: UserRoleUpdate,
    session: AsyncSession,
):
    user_to_upgrade = await get_user_by_user_id(
        user_id=user_id,
        session=session,
    )

    roles = user_to_upgrade.roles

    existing_roles = {role.id for role in roles}

    for name in update_data.role_names:

        role = await get_role_by_name(
            name,
            session,
        )

        if role.id not in existing_roles:
            roles.append(role)
            existing_roles.add(role.id)

    await session.commit()

    await session.refresh(user_to_upgrade)

    return user_to_upgrade
