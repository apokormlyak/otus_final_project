
greet = "Привет, {user_name}! Напиши мне название города и я пришлю сводку погоды"
menu = "📍 Главное меню"
url = "http://api.openweathermap.org/data/2.5/weather?q={message_text}&lang=ru&units=metric&appid={api_key}"
weather_reply = ("{today}\nПогода в городе: {city}\n"
                 "Температура: {cur_temp}°C {wd}\n"
                 "Влажность: {humidity}%\n"
                 "Давление: {math_pressure} мм.рт.ст\n"
                 "Ветер: {wind} м/с \n"
                 "Восход солнца: {sunrise_timestamp}\n"
                 "Закат солнца: {sunset_timestamp}\n"
                 "Продолжительность дня: {length_of_the_day}\n"
                 "Хорошего дня!")
exception_weather_reply = "Я не распознал город. Проверь название."
top_cities = ("Самые популярные по запросам города: \n"
              "{city_1}, количество запросов: {request_count_1},\n"
              "{city_2}, количество запросов: {request_count_2}")
