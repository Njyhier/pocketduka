import re
from pydantic import field_validator, BaseModel


class PhoneInput(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        phone = re.sub(r"\D", "", v)
        print(phone)

        if phone.startswith("254"):
            phone = phone[3:]

        if phone.startswith("+254"):
            phone = phone[4:]

        if phone.startswith("0"):
            phone = phone[1:]

        if not re.fullmatch(r"[17]\d{8}", phone):
            return {"message": f"{phone} is not a valid phone number"}

        phone = "254" + phone
        return phone
