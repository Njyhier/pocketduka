from fastapi import APIRouter, Depends
from app.schemas.Baseschema import ApiResponse
from app.schemas.inventory_schemas import (
    InventoryCreate,
    InventoryUpdate,
    InventoryRead,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.inventory_service import (
    create_inventory,
    get_inventories,
    get_inventory_by_id,
    update_inventory,
    delete_inventory,
)

router = APIRouter()


@router.post("/inventories", response_model=ApiResponse[InventoryRead])
async def add_inventory(
    inventory_data: InventoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await create_inventory(inventory_data=inventory_data, session=session)
    return {
        "message": "Inventory added successfully",
        "payload": payload,
    }


@router.get("/inventories", response_model=ApiResponse[list[InventoryRead]])
async def read_inventories(
    session: AsyncSession = Depends(get_async_session),
):
    inventories = await get_inventories(session=session)
    return {
        "message": "Inventories retrieved successfully",
        "payload": inventories,
    }


@router.get("/inventories/{inventory_id}", response_model=ApiResponse[InventoryRead])
async def read_inventory_by_id(
    inventory_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    inventory = await get_inventory_by_id(inventory_id=inventory_id, session=session)
    return {
        "message": "Retrieve inventory successful",
        "payload": inventory,
    }


@router.patch("/inventories/{inventory_id}", response_model=ApiResponse[InventoryRead])
async def patch_inventory(
    inventory_id: str,
    patch_data: InventoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    payload = await update_inventory(
        inventory_id=inventory_id,
        update_data=patch_data,
        session=session,
    )
    return {
        "message": "Inventory updated successfully",
        "payload": payload,
    }


@router.delete("/inventories/{inventory_id}", response_model=ApiResponse)
async def remove_inventory(
    inventory_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_inventory(inventory_id=inventory_id, session=session)
