from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

menu = [
    [InlineKeyboardButton(text='Узнать погоду', callback_data='get_weather')],
    [InlineKeyboardButton(text='Мои самые любимые города', callback_data='users_top_cities_requests')],
    [InlineKeyboardButton(text='Самые запрашиваемые города', callback_data='top_cities_requests')]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
