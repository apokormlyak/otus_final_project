import logging

from sqlalchemy import insert, select, update, BinaryExpression, BooleanClauseList, ColumnOperators
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import User, Cities
from ..database.schemes import Users as UserCreateScheme
from ..database.schemes import CityRequest as CityCreateScheme


logger = logging.getLogger(__name__)


async def create_user(session: AsyncSession, login: str):
    result = await session.execute(select(User).where(User.login == login))
    user = result.scalars().first()
    if user is None:
        usr = UserCreateScheme(login=login)
        stmt = insert(User).values(**usr.dict())
        await session.execute(stmt)
        await session.commit()
    return user


async def get_user(session: AsyncSession, filters: None | list[BinaryExpression
                                                               | BooleanClauseList | ColumnOperators] = None):
    user = None
    try:
        stmt = select(User)
        if filters:
            stmt = stmt.where(*filters)
            result = await session.execute(stmt)
            user = result.scalars().first()
    except:
        logger.exception(f'Исключение в get_user, filters: {filters} ')
    return user


async def update_user(session: AsyncSession, user_login: str, **kwargs):
    is_updated = False
    try:
        stmt = update(User).where(User.login == user_login).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except:
        logger.exception(f'Исключение в update_user, user_login: {user_login} ')
    return is_updated


async def update_user_favorites(session: AsyncSession, user_login: str, city_name):
    is_updated = False

    result = await session.execute(select(User).where(User.login == user_login))
    user = result.scalars().first()
    cities = user.favorite_cities
    cities = list(set(cities.append(city_name)))
    try:
        stmt = (
            update(User).
            where(User.login == user_login).
            values(favorite_cities=cities)
        )
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except:
        logger.exception(f'Исключение в update_user, user_login: {user_login} ')
    return is_updated


async def create_city(session: AsyncSession, name: str):
    result = await session.execute(select(Cities).where(Cities.name == name))
    city = result.scalars().first()
    if city is None:
        c = CityCreateScheme(name=name, requests_count=0)
        stmt = insert(Cities).values(**c.dict())
        await session.execute(stmt)
        await session.commit()
    return city


async def get_city(session: AsyncSession, filters: None | list[BinaryExpression
                                                               | BooleanClauseList | ColumnOperators] = None):
    city = None
    try:
        stmt = select(Cities)
        if filters:
            stmt = stmt.where(*filters)
            result = await session.execute(stmt)
            city = result.scalars().first()
    except:
        logger.exception(f'Исключение в get_city, filters: {filters} ')
    return city


async def update_city(session: AsyncSession, name: str, **kwargs):
    is_updated = False
    try:
        stmt = update(Cities).where(Cities.name == name).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except:
        logger.exception(f'Исключение в update_city, city_name: {name} ')
    return is_updated


async def increase_city_counter(session: AsyncSession, name: str):
    is_updated = False
    try:
        stmt = (
            update(Cities).
            where(Cities.name == name).
            values(requests_count=Cities.requests_count + 1)
        )
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except:
        logger.exception(f'Исключение в increase_city_counter, city_name: {name} ')
    return is_updated