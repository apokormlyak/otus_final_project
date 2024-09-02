import math
import os
import logging

import asyncio
import datetime

import requests
from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters import Command

from aiogram import types
from helpers.scripts.get_emoji import get_emoji
from helpers.crud.crud import (create_user, create_city,
                               update_user_data, increase_city_counter)
from helpers.database import get_async_session

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TOKEN')
api_key = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    @dp.message(Command("start"))
    async def start_command(message: types.Message):

        async for session in get_async_session():
            user = await create_user(login=message.dict()['chat']['username'], session=session)
            await message.reply(f"Привет, {message.dict()['chat']['first_name']}!"
                                f" Напиши мне название города и я пришлю сводку погоды")

    @dp.message()
    async def get_weather(message: types.Message):
        try:
            async for session in get_async_session():
                url = (f"http://api.openweathermap.org/data/"
                       f"2.5/weather?q={message.text}&lang=ru&units=metric&appid={api_key}")
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

                await create_city(session=session, name=data["name"])
                await increase_city_counter(session=session, name=data["name"])
                await update_user_data(session=session,
                                       user_login=message.dict()['chat']['username'],
                                       city_name=data["name"])

                await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                                    f"Погода в городе: {city}\n"
                                    f"Температура: {cur_temp}°C {wd}\n"
                                    f"Влажность: {humidity}%\n"
                                    f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
                                    f"Ветер: {wind} м/с \n"
                                    f"Восход солнца: {sunrise_timestamp}\n"
                                    f"Закат солнца: {sunset_timestamp}\n"
                                    f"Продолжительность дня: {length_of_the_day}\n"
                                    f"Хорошего дня!"
                                    )
        except:
            await message.reply("Я не распознал город. Проверь название.")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
