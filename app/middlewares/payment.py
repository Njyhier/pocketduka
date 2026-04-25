from dotenv import load_dotenv
from datetime import datetime
import requests
import base64
import os

load_dotenv()


def get_access_token():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    print(consumer_key, "and", consumer_secret)
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(url, headers=headers)
    print("RES", response)

    print("STATUS:", response.status_code)
    print("HEADERS:", response.headers)
    print("RAW TEXT:", response.text[:500])

    try:
        data = response.json()
        print("DATA", data)
        return data.get("access_token")
    except Exception as e:
        print("JSON ERROR:", e)
        return None


def gen_password():
    shortcode = "174379"
    passkey = os.getenv("PASSKEY")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = shortcode + passkey + timestamp
    password = base64.b64encode(data.encode()).decode()
    print(password)
    print(timestamp)

    return password, timestamp


def stk_push(phone: str, amt: str):
    print("INITIATING STK PUSH")
    [password, timestamp] = gen_password()
    access_token = get_access_token()
    url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amt,
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://pocketduka.onrender.com/callback",
        "AccountReference": "accountref",
        "TransactionDesc": "txndesc",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
