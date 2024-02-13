from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert, select, values, update
from database.db import async_session_factory

from auth.utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from auth.models import User
import auth.schemas as schemas


router = APIRouter(tags=['users'])


@router.get('/')
async def get_user_list():
    async with async_session_factory() as session:
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users


@router.post('/')
async def create_user(user: schemas.UserCreate) -> schemas.User:
    async with async_session_factory() as session:
        user_data = user.model_dump(exclude_unset=True)
        query = select(User).filter_by(login=user_data.get('login'))
        username_result = await session.execute(query)
        db_username = username_result.scalars().all()
        if len(db_username) > 0:
            raise HTTPException(
                status_code=400, detail="Login is already in use")
        user_data['password'] = await get_hashed_password(user_data.get('password'))
        db_user = User(**user_data)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


@router.post('/login/')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    async with async_session_factory() as session:

        query = select(User).filter_by(login=form_data.username)
        db_user = await session.execute(query)
        user_to_login = db_user.scalars().all()[0]
        if not user_to_login:
            raise HTTPException(
                status_code=404, detail="User dosent exist")
        hashed_pass = user_to_login.password
        if not await verify_password(form_data.password, hashed_pass=hashed_pass):
            raise HTTPException(
                status_code=404, detail="Password is incorrect")
        return {
            'access_token': await create_access_token(user_to_login.login),
            'refresh_token': await create_refresh_token(user_to_login.login),
        }


@router.get('/{user_id}/')
async def get_user(user_id: int) -> schemas.User:
    async with async_session_factory() as session:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
