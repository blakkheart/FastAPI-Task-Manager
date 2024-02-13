from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
import uvicorn
from sqlalchemy import and_, insert, select, values, update
from database.db import async_session_factory, Base
from models import Task
import schemas
from auth.crud import router as user_router
from auth.deps import get_current_user
from auth.schemas import User

app = FastAPI()
app.include_router(user_router, prefix='/users')


@app.get('/tasks/')
async def get_task_list(
    user: User = Depends(get_current_user)
) -> List[schemas.Task]:
    async with async_session_factory() as session:
        query = select(Task).where(Task.author_id == user.id)
        result = await session.execute(query)
        db_tasks = result.scalars().all()
        return db_tasks


@app.post('/tasks/')
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


@app.get('/task/{task_id}/')
async def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
) -> schemas.Task:
    async with async_session_factory() as session:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.author_id == user.id))
        result = await session.execute(query)
        db_task = result.scalars().first()
        print(db_task)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return db_task


@app.patch('/task/{task_id}/')
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
        for key, val in task_data.items():
            setattr(db_task, key, val)
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task


@app.delete('/task/{task_id}/')
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


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
