from sqlalchemy.orm import Mapped

from .db import Base
from sqlalchemy import String, Integer, Column, ARRAY


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    login: Mapped[str] = Column(String(length=128), index=True, nullable=False, unique=True)
    favorite_cities = Column(ARRAY(Integer), nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r})"


class Cities(Base):
    __tablename__ = 'city'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(length=128), index=True, nullable=False, unique=True)
    requests_count: Mapped[int] = Column(Integer)

    def __repr__(self) -> str:
        return f"City(id={self.id!r}, name={self.name!r}, requests_count = {self.requests_count})"
