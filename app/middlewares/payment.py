from dotenv import load_dotenv
from datetime import datetime
import requests
import base64
import os
import httpx

load_dotenv()


async def get_access_token():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    print(consumer_key, "and", consumer_secret)
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    headers = {"Authorization": f"Basic {encoded_credentials}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print("RES", response)

        try:
            data = response.json()
            return data.get("access_token")
        except Exception as e:
            print("JSON ERROR:", e)
            return None


async def gen_password():
    shortcode = "174379"
    passkey = os.getenv("PASSKEY")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = shortcode + passkey + timestamp
    password = base64.b64encode(data.encode()).decode()
    print(password)
    print(timestamp)

    return password, timestamp


async def stk_push(amt: str, phone: str):
    print("INITIATING STK PUSH")
    password, timestamp = await gen_password()
    access_token = await get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amt,
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://app.mconnect.africa/pocket/callback",
        "AccountReference": "accountref",
        "TransactionDesc": "txndesc",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()
        print("STKPUSH", data)
        return data
