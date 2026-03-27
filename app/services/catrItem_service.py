from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from app.services import cart_service, product_service
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.models.cart import Cart


async def get_item_by_id(item_id: str, session: AsyncSession) -> CartItem:
    result = await session.execute(
        select(CartItem)
        .where(CartItem.id == item_id)
        .options(
            selectinload(CartItem.product).selectinload(Product.inventories),
        ),
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


async def create_cart_item(
    product_id: str, cart_id: str, session: AsyncSession
) -> CartItem:
    product = await product_service.get_product_by_id(
        product_id=product_id, session=session
    )
    cart = await cart_service.get_cart_by_id(cart_id=cart_id, session=session)
    item = CartItem(
        product_id=product.id,
        cart_id=cart.id,
        price=product.inventories[0].selling_price,
        image_url=product.images[0].url if product.images else None,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_cart_item(item_id, session: AsyncSession):
    item = await get_item_by_id(item_id=item_id, session=session)
    if item:
        await session.execute(delete(CartItem).where(CartItem.id == item.id))
    return {"status": 200, "message": "Item removed from cart"}


async def increment_item_quantity(item_id: str, session: AsyncSession):
    item = await get_item_by_id(item_id=item_id, session=session)
    item.increment_quantity()
    await session.commit()
    await session.refresh(item)
    return item.quantity


async def decrement_item_quantity(item_id: str, session: AsyncSession):
    item = await get_item_by_id(item_id=item_id, session=session)
    if item.quantity > 0:
        item.decrement_quantity()
    else:
        await delete_cart_item(item_id=item.id, session=session)
    await session.commit()
    await session.refresh(item)
    return item.quantity


async def item_in_cart(user: User, inventory_id: str):
    return next(
        (
            item
            for item in user.cart.items
            if item.product.inventories[0].id == inventory_id
        ),
        None,
    )


async def add_item_to_cart(product_id: str, cart_id: str, session: AsyncSession):
    res = await session.execute(
        select(CartItem).where(CartItem.product_id == product_id)
    )
    item = res.scalar_one_or_none()
    if item is not None:
        item.increment_quantity()
        await session.commit()
        await session.refresh(item)
        return item.quantity
    else:
        return await create_cart_item(
            product_id=product_id, cart_id=cart_id, session=session
        )

    # return {"status": 200, "message": "Item added to cart successfully"}
