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

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TOKEN')
api_key = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        logger.info(message)
        await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")

    @dp.message()
    async def get_weather(message: types.Message):
        try:
            url = (f"http://api.openweathermap.org/data/"
                   f"2.5/weather?q={message.text}&lang=ru&units=metric&appid={api_key}")
            response = requests.get(url)
            data = response.json()
            print(data)
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
