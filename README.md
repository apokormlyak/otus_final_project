# otus_final_project

Телеграмм-бот - Синоптик

t.me/SuperEasyWeatherBot 


## Для создания собственного бота: 

Ключ для Telegram-бота можно получить у @BotFather, введя /newbot — команду для создания и регистрации нового бота.

API для запрашивания погоды:  https://openweathermap.org/current


__________________________________________________________


## Для запуска локального запуска приложения:

1. Запустить бот: docker-compose up --build

## Для накатывания миграций

1. docker exec -it tele_bot alembic revision --autogenerate


__________________________________________________________
