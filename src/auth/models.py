import datetime
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class User(Base):
    __tablename__ = 'user_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(25))
    password: Mapped[str]
    email: Mapped[str | None] = mapped_column(default=None)
    first_name: Mapped[str | None] = mapped_column(String(50), default=None)
    last_name: Mapped[str | None] = mapped_column(String(50), default=None)

    registred_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow)

    task: Mapped[List['Task']] = relationship(back_populates='author')
