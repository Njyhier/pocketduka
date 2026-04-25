from sqlalchemy.ext.asyncio import AsyncSession
from app.services.payment_service import get_payment_by_checkout_id, create_payment
from fastapi import HTTPException, status, Depends
from app.db.session import get_async_session
from fastapi import APIRouter
from app.schemas.payment_schema import PaymentCreate, PaymentRead, Data
from app.schemas.Baseschema import ApiResponse

router = APIRouter()


@router.post("/payments")
async def make_payment(
    data: Data,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_payment(payment_data=data, session=session)


@router.post("/mpesa/callback")
async def mpesa_callback(
    data: dict,
    session: AsyncSession = Depends(get_async_session),
):
    print("CALLBACK HIT", data)
    callback = data["Body"]["stkCallback"]

    checkout_request_id = callback["CheckoutRequestID"]
    result_code = callback["ResultCode"]
    result_desc = callback["ResultDesc"]
    print(checkout_request_id)

    # Find payment by checkout_request_id
    payment = await get_payment_by_checkout_id(checkout_request_id, session)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if result_code == 0:
        payment.status = "successful"

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
    print("PAYMENT Status", payment.status)
    await session.commit()

    return {"message": "Callback processed"}
