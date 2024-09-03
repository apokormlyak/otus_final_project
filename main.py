import math
import os
import logging

import asyncio
import datetime

import requests
from aiogram import Bot, F
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters import Command

from aiogram import types
from aiogram.types import CallbackQuery

from helpers.scripts.get_emoji import get_emoji
from helpers.crud.crud import (create_user, create_city,
                               update_user_data, increase_city_counter,
                               get_top_cities_requests, get_users_data)
from helpers.database import get_async_session
from helpers.scripts import messages, keyboard

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TOKEN')
api_key = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    @dp.message(Command("start"))
    async def start_command(message: types.Message):

        async for session in get_async_session():
            global user_login
            user_login = message.dict()['chat']['username']
            user = await create_user(login=user_login, session=session)
            user_name = message.dict()['chat']['first_name']
            await message.reply(messages.greet.format(user_name=user_name), reply_markup=keyboard.menu)

    @dp.message(F.text == 'Меню')
    @dp.message(F.text == 'Выйти в меню')
    @dp.message(F.text == '◀️ Выйти в меню')
    async def menu(message: types.Message):
        await message.reply(messages.menu, reply_markup=keyboard.menu)

    @dp.callback_query(F.data == "get_weather")
    async def get_weather(clbck: CallbackQuery):
        await clbck.message.answer(messages.get_weather)

    @dp.callback_query(F.data == "users_top_cities_requests")
    async def users_top_cities_requests(clbck: CallbackQuery):
        try:
            async for session in get_async_session():
                data = await get_users_data(user_login=user_login, session=session)
                if data:
                    cities = ', '.join(data)
                    logger.exception(cities)
                    await clbck.message.answer(messages.users_top_cities_requests + cities, reply_markup=keyboard.menu)
                else:
                    await clbck.message.answer(messages.users_top_cities_requests_first_meet)
        except NameError:
            await clbck.message.answer(messages.greet_unknown_user)

    @dp.callback_query(F.data == "top_cities_requests")
    async def top_cities_requests(clbck: CallbackQuery):

        async for session in get_async_session():
            cities = await get_top_cities_requests(session=session)
            city_1 = cities[0].name
            city_2 = cities[1].name
            request_count_1 = cities[0].requests_count
            request_count_2 = cities[1].requests_count
            await clbck.message.answer(messages.top_cities.format(
                city_1=city_1,
                city_2=city_2,
                request_count_1=request_count_1,
                request_count_2=request_count_2
            ), reply_markup=keyboard.exit_kb)

    @dp.message()
    async def get_weather(message: types.Message):
        try:
            async for session in get_async_session():
                message_text = message.text
                url = (messages.url.format(message_text=message_text,
                                           api_key=api_key))
                response = requests.get(url)
                data = response.json()
                city = data["name"]
                cur_temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]

                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

                length_of_the_day = datetime.datetime.fromtimestamp(
                    data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"])
                wd = get_emoji(data)
                today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                math_pressure = math.ceil(pressure / 1.333)

                await create_city(session=session, name=data["name"])
                await increase_city_counter(session=session, name=data["name"])
                await update_user_data(session=session,
                                       user_login=message.dict()['chat']['username'],
                                       city_name=data["name"])
                await message.answer(
                    messages.weather_reply.format(
                        today=today, city=city,
                        cur_temp=cur_temp, wd=wd,
                        humidity=humidity, math_pressure=math_pressure,
                        wind=wind, sunrise_timestamp=sunrise_timestamp,
                        sunset_timestamp=sunset_timestamp,
                        length_of_the_day=length_of_the_day
                    )
                )
        except:
            await message.answer(messages.exception_weather_reply)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
