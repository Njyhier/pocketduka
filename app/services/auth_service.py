import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.access_token import (
    secret_key,
    algorithm,
    token_validity_minutes,
    create_access_token,
)
from app.utils.user_utils import get_user_by_username
from app.utils.password import verify_password, password_hash
from typing import Annotated

from app.models.user import User
from datetime import timedelta
from app.db.session import get_async_session
from app.schemas.token_schemas import TokenData, Token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
dummy_password = "dummypass"
dummy_hash = password_hash.hash(dummy_password)


async def authenticate_user(username: str, plain_password: str, session: AsyncSession):
    user = await get_user_by_username(username, session)
    if user is None:
        await verify_password(dummy_password, dummy_hash)
        return False
    if not await verify_password(plain_password, user.password_hash):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("Get current user called")
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(payload)
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print(token_data)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(username=token_data.username, session=session)
    print(user)
    if user is None:
        raise credentials_exception
    return user


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession,
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token_validity_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(access_token)
    token = Token(access_token=access_token, token_type="bearer")
    return token
    return {
        "message": "Login successful",
        "payload": {
            "token": token,
            "user": user,
        },
    }


async def get_current_user_dep(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_current_user(token, session)


async def get_user_roles(user: User = Depends(get_current_user)):
    user_roles = {role.name for role in user.roles}
    return user_roles


def require_roles_dep(*roles: str):
    async def check_roles(user_roles: set[str] = Depends(get_user_roles)):
        if not any(name in user_roles for name in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user_roles

    return check_roles


async def get_current_user_roles(user):
    roles = [role.name for role in user.roles]
    return roles
