import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from auth.models import User
from auth.utils import JWT_SECRET_KEY, ALGORITHM
from jose import jwt
from pydantic import ValidationError
from auth.schemas import TokenPayload, UserCreate, SystemUser
from database.db import async_session_factory


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl='/users/login/',
    scheme_name='JWT'
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    async with async_session_factory() as session:
        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if datetime.datetime.fromtimestamp(token_data.exp) < datetime.datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        query = select(User).filter_by(login=token_data.sub)
        db_user = await session.execute(query)
        user_to_login = db_user.scalars().all()[0]
        if not user_to_login:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return user_to_login
