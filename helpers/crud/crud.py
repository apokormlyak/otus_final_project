import logging

from asyncpg import ForeignKeyViolationError
from sqlalchemy import insert, select, update, BinaryExpression, BooleanClauseList, ColumnOperators
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from ..database.models import User, Cities, UserData
from ..database.schemes import Users as UserCreateScheme
from ..database.schemes import CityRequest as CityCreateScheme
from ..database.schemes import UserData as UserDataScheme
from translate import Translator
from ..scripts.language import detect

translator = Translator(to_lang="ru", from_lang='en')

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
    stmt = select(User)
    if filters:
        stmt = stmt.where(*filters)
        result = await session.execute(stmt)
        user = result.scalars().first()
    return user


async def update_user(session: AsyncSession, user_login: str, **kwargs):
    is_updated = False
    result = await session.execute(select(User).where(User.login == user_login))
    user = result.scalars().first()
    if user is not None:
        stmt = update(User).where(User.login == user_login).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    return is_updated


async def get_users_data(session: AsyncSession, user_login: str):
    stmt = select(Cities.name).join(UserData).where(UserData.user_login == user_login)
    result = await session.execute(stmt)
    data = result.scalars().all()
    return data


async def update_user_data(session: AsyncSession, user_login: str, city_name):
    is_updated = False
    if detect(city_name) == 'en':
        city_name = translator.translate(city_name)
        logger.exception(city_name)

    city = await get_city(session, filters=[Cities.name == city_name.lower()])
    result = await session.execute(select(User).where(User.login == user_login))
    user = result.scalars().first()
    if user is not None:
        result = await session.execute(select(UserData).filter(
            and_(
                UserData.user_login == user_login,
                UserData.city_id == city.id)
        )
        )

        res = result.scalars().first()

        if res is None:
            data = UserDataScheme(user_login=user_login, city_id=city.id)
            stmt = insert(UserData).values(**data.dict())
            await session.execute(stmt)
            await session.commit()
            is_updated = True
    return is_updated


async def create_city(session: AsyncSession, name: str):
    if detect(name) == 'en':
        name = translator.translate(name)
    result = await session.execute(select(Cities).where(Cities.name == name.lower()))
    city = result.scalars().first()
    if city is None:
        c = CityCreateScheme(name=name.lower(), requests_count=0)
        stmt = insert(Cities).values(**c.dict())
        await session.execute(stmt)
        await session.commit()
    return city


async def get_city(session: AsyncSession, filters: None | list[BinaryExpression
                                                               | BooleanClauseList | ColumnOperators] = None):
    stmt = select(Cities)
    if filters:
        stmt = stmt.where(*filters)
        result = await session.execute(stmt)
        city = result.scalars().first()
        return city


async def get_top_cities_requests(session: AsyncSession):
    stmt = select(Cities).order_by(Cities.requests_count.desc()).limit(3)

    result = await session.execute(stmt)
    cities = result.scalars().all()
    return cities


async def update_city(session: AsyncSession, name: str, **kwargs):
    if detect(name) == 'en':
        name = translator.translate(name)
    is_updated = False
    try:
        stmt = update(Cities).where(Cities.name == name).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except ForeignKeyViolationError:
        logger.exception(f'Исключение в update_city, city_name: {name} ')
    return is_updated


async def increase_city_counter(session: AsyncSession, name: str):
    if detect(name) == 'en':
        name = translator.translate(name)
    is_updated = False
    try:
        stmt = (
            update(Cities).
            where(Cities.name == name.lower()).
            values(requests_count=Cities.requests_count + 1)
        )
        await session.execute(stmt)
        await session.commit()
        is_updated = True
    except ForeignKeyViolationError:
        logger.exception(f'Исключение в increase_city_counter, city_name: {name} ')
    return is_updated
