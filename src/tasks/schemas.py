import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    text: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_done: bool

    class Config:
        orm_model = True


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    is_done: Optional[bool] = None
