from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_validity_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
