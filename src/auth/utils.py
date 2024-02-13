import logging
import datetime
from typing import Any, Union

from passlib.context import CryptContext
from jose import jwt

from config import settings

logging.getLogger('passlib').setLevel(logging.ERROR)

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY


async def create_access_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
