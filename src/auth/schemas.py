import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    registred_at: datetime.datetime

    class Config:
        orm_model = True


class UserUpdate(BaseModel):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class SystemUser(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
