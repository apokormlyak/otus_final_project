from sqlalchemy.orm import Mapped

from .db import Base
from sqlalchemy import String, Integer, Column, ForeignKey


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    login: Mapped[str] = Column(String(length=128), index=True, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, favorite_cities={self.favorite_cities!r})"


class Cities(Base):
    __tablename__ = 'city'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(length=128), index=True, nullable=False, unique=True)
    requests_count: Mapped[int] = Column(Integer)

    def __repr__(self) -> str:
        return f"City(id={self.id!r}, name={self.name!r}, requests_count = {self.requests_count})"


class UserData(Base):
    __tablename__ = 'user_data'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_login = Column(ForeignKey("user.login", ondelete="CASCADE"), index=True, nullable=True)
    city_id = Column(ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=True)