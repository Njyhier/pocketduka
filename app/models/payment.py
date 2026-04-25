from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel
from datetime import datetime, timezone
import uuid
from sqlalchemy.sql import func


class Payment(BaseModel):
    __tablename__ = "payments"

    id = Column(
        String(60),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    phone_number = Column(
        String,
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    status = Column(
        String,
        default="PENDING",
    )

    mpesa_receipt_number = Column(
        String,
        nullable=True,
    )

    checkout_request_id = Column(
        String,
        unique=True,
        index=True,
    )

    merchant_request_id = Column(
        String,
        nullable=True,
    )

    result_code = Column(
        String,
        nullable=True,
    )

    result_desc = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    order = relationship(
        "Order",
        back_populates="payment",
    )
    user = relationship(
        "User",
        back_populates="payments",
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
    )
