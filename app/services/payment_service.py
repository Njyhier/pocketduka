from app.schemas.payment_schema import PaymentCreate
from fastapi import HTTPException, status
from app.schemas.order_schema import OrderRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.payment import stk_push
from app.models.payment import Payment
from sqlalchemy import select


async def create_payment(payment_data: dict, session: AsyncSession):
    user_id = payment_data["user_id"]
    phone_number = payment_data["phone_number"]
    amount = payment_data["amount"]

    response = stk_push(phone=phone_number, amt=amount)

    # Initial request response
    checkout_request_id = response["CheckoutRequestID"]
    merchant_request_id = response["MerchantRequestID"]
    # print("MERCHANT", merchant_request_id)

    payment = Payment(
        status="pending",
        phone_number=phone_number,
        checkout_request_id=checkout_request_id,
        merchant_request_id=merchant_request_id,
        user_id=user_id,
        amount=float(amount),
    )
    # print("PAYMENT CID", payment.checkout_request_id)

    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return {"message": "payment registered"}


async def get_payment_by_checkout_id(checkout_request_id: str, session: AsyncSession):
    result = await session.execute(
        select(Payment).where(Payment.checkout_request_id == checkout_request_id)
    )
    payment = result.scalar_one_or_none()
    print(payment.checkout_request_id)
    return payment
