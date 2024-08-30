# otus_final_project

Телеграмм-бот - Синоптик

t.me/SuperEasyWeatherBot 


## Для создания собственного бота: 

Ключ для Telegram-бота можно получить у @BotFather, введя /newbot — команду для создания и регистрации нового бота.

API для запрашивания погоды:  https://openweathermap.org/current


## Для запуска локального запуска приложения:

1. Запустить postgres: docker-compose up --build


__________________________________________________________

### Для инициализации алембик:
1. alembic init -t async alembic
2. alembic revision --autogenerate
3. alembic upgrade head