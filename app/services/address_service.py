from app.schemas.address_schemas import (
    AddressCreate,
    AddressUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.services.auth_service import get_current_user_dep
from app.models.address import Address
from sqlalchemy import select


async def get_address_by_id(
    address_id: str,
    session: AsyncSession,
) -> Address:
    result = await session.execute(
        select(Address).where(Address.id == address_id),
    )
    address = result.scalar_one_or_none()
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return address


async def create_address(
    address_data: AddressCreate,
    session: AsyncSession,
    user: User,
) -> Address:
    db_address = Address(**address_data.model_dump())
    db_address.users.append(user)
    session.add(db_address)
    await session.commit()
    await session.refresh(db_address)
    return db_address


async def read_addresses(session):
    result = await session.execute(select(Address).options(selectinload(Address.users)))
    addresses = result.scalars()
    return addresses


async def delete_address(address_id: str, session: AsyncSession):
    address_to_delete = await get_address_by_id(address_id=address_id, session=session)
    await session.delete(address_to_delete)
    await session.commit()
    return {"status": 200, "message": "Address deleted successfully"}


async def update_address(
    address_id: str,
    update_data: AddressUpdate,
    session: AsyncSession,
):
    address_to_update = await get_address_by_id(
        address_id=address_id,
        session=session,
    )
    update_data = update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address_to_update, key, value)
    await session.commit()
    await session.refresh(address_to_update)
    return address_to_update
