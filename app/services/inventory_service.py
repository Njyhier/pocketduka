from app.schemas.inventory_schemas import (
    InventoryCreate,
    InventoryUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from sqlalchemy import select


async def get_inventory_by_id(inventory_id: str, session: AsyncSession) -> Inventory:
    result = await session.execute(
        select(Inventory).where(Inventory.id == inventory_id)
    )
    inventory = result.scalar_one_or_none()
    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found",
        )
    return inventory


async def create_inventory(
    inventory_data: InventoryCreate, session: AsyncSession
) -> Inventory:
    db_inventory = Inventory(**inventory_data.model_dump())
    session.add(db_inventory)
    await session.commit()
    await session.refresh(db_inventory)
    return db_inventory


async def update_inventory(
    inventory_id: str, update_data: InventoryUpdate, session: AsyncSession
) -> Inventory:
    inventory_to_update = await get_inventory_by_id(
        inventory_id=inventory_id, session=session
    )
    update_data = update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inventory_to_update, key, value)
    await session.commit()
    await session.refresh(inventory_to_update)
    return inventory_to_update


async def delete_inventory(inventory_id: str, session: AsyncSession):
    inventory_to_delete = await get_inventory_by_id(
        inventory_id=inventory_id, session=session
    )
    await session.delete(inventory_to_delete)
    await session.commit()
    return {"message": "Inventory Deleted successfully"}


async def get_inventories(session: AsyncSession) -> list[Inventory]:
    result = await session.execute(select(Inventory))
    inventories = result.scalars().all()
    return inventories
