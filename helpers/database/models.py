from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from db import Base
from sqlalchemy import String
from sqlalchemy import Integer
from typing import List


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100))
    favorite_cities: Mapped[List["Cities"]] =\
        relationship(back_populates="id", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r})"


class Cities(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True, back_populates="favorite_cities")
    name: Mapped[str] = mapped_column(String(70))
    requests_count: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"City(id={self.id!r}, name={self.name!r}, requests_count = {self.requests_count})"
