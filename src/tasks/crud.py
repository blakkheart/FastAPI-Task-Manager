import datetime
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy import and_, insert, select, values, update
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, add_pagination

from src.database.db import async_session_factory, Base
from src.tasks.models import Task
import src.tasks.schemas as schemas
from src.auth.deps import get_current_user
from src.auth.schemas import User


router = APIRouter(tags=['tasks'])


@router.get('/')
async def get_task_list(
    user: User = Depends(get_current_user),
    done: bool = None,
    limit: int = 100,
    offset: int = 0,
) -> List[schemas.Task]:
    async with async_session_factory() as session:
        if done is None:
            query = (
                select(Task)
                .where(Task.author_id == user.id)
                .order_by(Task.created_at)
                .limit(limit)
                .offset(offset)
            )
        else:
            query = (
                select(Task)
                .filter(and_(Task.author_id == user.id, Task.is_done == done))
                .order_by(Task.created_at)
                .limit(limit)
                .offset(offset)
            )
        result = await session.execute(query)
        db_tasks = result.scalars().all()
        if not db_tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
        return db_tasks


@router.post('/')
async def create_task(
    text: schemas.TaskCreate,
    user: User = Depends(get_current_user),
) -> schemas.Task:
    async with async_session_factory() as session:
        db_task = Task(text=text.text, author=user)
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task


@router.get('/{task_id}/')
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
) -> schemas.Task:
    async with async_session_factory() as session:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.author_id == user.id))
        result = await session.execute(query)
        db_task = result.scalars().first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return db_task


@router.patch('/{task_id}/')
async def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    user: User = Depends(get_current_user),
) -> schemas.Task:
    async with async_session_factory() as session:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.author_id == user.id))
        result = await session.execute(query)
        db_task = result.scalars().first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        task_data = task.model_dump(exclude_unset=True)
        task_data['updated_at'] = datetime.datetime.utcnow()
        for key, val in task_data.items():
            setattr(db_task, key, val)
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task


@router.delete('/{task_id}/')
async def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
) -> Response:
    async with async_session_factory() as session:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.author_id == user.id))
        result = await session.execute(query)
        db_task = result.scalars().first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        await session.delete(db_task)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
