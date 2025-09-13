# Импортируем необходимые модули
import asyncio  # для работы с асинхронными функциями
import logging  # для ведения логов
import sys      # для доступа к стандартным потокам ввода/вывода
from os import getenv  # для получения переменных окружения

# Импортируем aiogram — фреймворк для Telegram ботов
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Получаем токен бота из переменной окружения BOT_TOKEN
# Это безопасный способ не хранить токен в коде
TOKEN = getenv("BOT_TOKEN")

# Создаем экземпляр Dispatcher
# Dispatcher управляет обработкой всех событий бота (команды, сообщения, inline-кнопки)
dp = Dispatcher()


# Основная асинхронная функция запуска бота
async def main() -> None:
    """
    Запускает Telegram бота с использованием aiogram.
    
    Логика:
    1. Создаем объект Bot с токеном и настройками по умолчанию
       (parse_mode=HTML позволяет использовать HTML-теги в сообщениях)
    2. Запускаем long polling через Dispatcher, чтобы бот слушал входящие сообщения
    """
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # устанавливаем HTML как формат текста
    )

    # Запускаем обработку входящих событий
    await dp.start_polling(bot)


# Точка входа скрипта
if __name__ == "__main__":
    # Настраиваем логирование в консоль с уровнем INFO
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Запускаем асинхронную функцию main через asyncio
    asyncio.run(main())
