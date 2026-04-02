from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schemas.Baseschema import ApiResponse
from app.schemas.address_schemas import AddressCreate, AddressUpdate, AddressRead
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.address_service import (
    create_address,
    get_address_by_id,
    delete_address,
    update_address,
    read_addresses,
)

router = APIRouter()


@router.post("/addresses", response_model=ApiResponse[AddressRead])
async def add_address(
    address_data: AddressCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    payload = await create_address(
        address_data=address_data, session=session, user=user
    )
    return {
        "status": 200,
        "message": "Address added successfully",
        "payload": payload,
    }


@router.get("/addresses", response_model=ApiResponse[list[AddressRead]])
async def get_addresses(
    session: AsyncSession = Depends(get_async_session),
):
    addresses = await read_addresses(session=session)
    return {
        "status": 200,
        "message": "Addresses retrieved successfully",
        "payload": addresses,
    }


@router.get("/addresses/{address_id}", response_model=ApiResponse[AddressRead])
async def read_address_by_id(
    address_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    address = await get_address_by_id(address_id=address_id, session=session)
    return {
        "status": 200,
        "message": "Retrieve address successful",
        "payload": address,
    }


@router.patch("/addresses/{address_id}", response_model=ApiResponse[AddressRead])
async def patch_address(
    address_id: str,
    patch_data: AddressUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await update_address(
        address_id=address_id,
        update_data=patch_data,
        session=session,
    )
    return {
        "status": 200,
        "message": "Address updated successfully",
        "payload": payload,
    }


@router.delete("/addresses/{address_id}", response_model=ApiResponse)
async def remove_address(
    address_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_address(address_id=address_id, session=session)
