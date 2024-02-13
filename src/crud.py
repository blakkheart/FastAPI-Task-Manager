from database.db import async_engine, async_session_factory, Base
from sqlalchemy import select
from models import Task


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_task_list():
    async with async_session_factory() as session:
        query = select(Task)
        result = await session.execute(query)
        todos = result.scalars().all()
        return todos


async def create_task():
    async with async_session_factory() as session:
        pass
