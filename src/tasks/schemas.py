import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    registred_at: datetime.datetime


class TaskBase(BaseModel):
    text: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_done: bool
    # author_id: int
    # author: 'User'

    class Config:
        orm_model = True


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    is_done: Optional[bool] = None
