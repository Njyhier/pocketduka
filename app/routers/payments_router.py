from sqlalchemy.ext.asyncio import AsyncSession
from app.services.payment_service import (
    get_payment_by_checkout_id,
    create_payment,
    simulate_payment,
)
from fastapi import HTTPException, status, Depends
from app.db.session import get_async_session
from app.services.auth_service import get_current_user
from fastapi import APIRouter
from app.services.order_service import create_order_with_items
from app.schemas.payment_schema import PaymentCreate, PaymentRead, Data
from app.schemas.Baseschema import ApiResponse
from app.models.user import User

router = APIRouter()


@router.post("/users/{user_id}/payments")
async def make_payment(
    phone: str,
    data: Data,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_id = user.id
    payment_data = {
        "phone": phone,
        "user_id": user_id,
        "amount": data.amount,
    }
    return await create_payment(payment_data=payment_data, session=session)


@router.post("/callback")
async def mpesa_callback(
    data: dict,
    session: AsyncSession = Depends(get_async_session),
):
    # return await simulate_payment()
    print("CALLBACK HIT")
    callback = data["Body"]["stkCallback"]
    print("CALLBACK", callback)

    checkout_request_id = callback["CheckoutRequestID"]
    result_code = callback["ResultCode"]
    result_desc = callback["ResultDesc"]
    # print(checkout_request_id)

    payment = await get_payment_by_checkout_id(checkout_request_id, session)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status == "successful":
        return {
            "message": "Callback already processed",
            "payment status": payment.status,
        }

    if result_code == 0:
        payment.status = "successful"
        await create_order_with_items(
            user_id=payment.user_id,
            payment_id=payment.id,
            session=session,
        )

        items = callback.get("CallbackMetadata", {}).get("Item", [])

        for item in items:
            if item["Name"] == "MpesaReceiptNumber":
                payment.mpesa_receipt_number = item["Value"]
            elif item["Name"] == "TransactionDate":
                payment.transaction_date = item["Value"]
    else:
        payment.status = "failed"

    payment.result_code = result_code
    payment.result_desc = result_desc
    print("PAYMENT", payment.mpesa_receipt_number)
    await session.commit()
    await session.refresh(payment)

    return {
        "message": "Callback processed",
        "payload": payment.status,
    }
