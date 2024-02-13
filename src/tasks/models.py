from typing import Annotated
import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class Task(Base):
    __tablename__ = 'task_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow)
    is_done: Mapped[bool] = mapped_column(default=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    author: Mapped['User'] = relationship("User", back_populates="task")
