from app.schemas.payment_schema import PaymentCreate
from fastapi import HTTPException, status
from app.schemas.order_schema import OrderRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.middlewares.payment import stk_push
from app.models.payment import Payment
from sqlalchemy import select
import httpx


async def create_payment(payment_data: dict, session: AsyncSession):
    user_id = payment_data["user_id"]
    amount = payment_data["amount"]
    phone = payment_data["phone"]

    response = await stk_push(amt=amount, phone=phone)
    print("Response", response)

    # Initial request response
    if response:
        checkout_request_id = response["CheckoutRequestID"]
        merchant_request_id = response["MerchantRequestID"]
    # print("MERCHANT", merchant_request_id)

    payment = Payment(
        status="pending",
        phone_number="254708374149",
        checkout_request_id=checkout_request_id,
        merchant_request_id=merchant_request_id,
        user_id=user_id,
        amount=float(amount),
    )
    # print("PAYMENT CID", payment.checkout_request_id)

    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return {"message": "payment registered", "payload": payment}


async def get_payment_by_checkout_id(checkout_request_id: str, session: AsyncSession):
    result = await session.execute(
        select(Payment).where(Payment.checkout_request_id == checkout_request_id)
    )
    payment = result.scalar_one_or_none()
    print(payment.checkout_request_id)
    return payment


async def simulate_payment(data):
    url = "https://pocketduka.onrender.com/callback"
    async with httpx.AsyncClient() as client:
        res = await client.post(url=url, json=data)
        return res.json()
