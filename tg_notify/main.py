# ---------------------------------------------------------
# tg_notify: Telegram Bot + RabbitMQ (Faststream) интеграция
# ---------------------------------------------------------

# Импорт стандартных модулей
import asyncio          # Для работы с асинхронными функциями
import logging          # Для логирования событий в консоль
import sys              # Для доступа к стандартным потокам ввода/вывода
from os import getenv  # Для получения переменных окружения (например, токена бота)

# Импортируем aiogram — фреймворк для Telegram ботов
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# Импортируем брокер RabbitMQ из faststream
from faststream.rabbit import RabbitBroker

# -------------------------------
# Конфигурация бота
# -------------------------------

# Получаем токен бота
# В учебном проекте токен можно хранить в коде, в реальном проекте обязательно через переменные окружения
TOKEN = "8459032249:AAGUq1Pn8ntycEDpAQYym7ePKjTAXfwN74s"

# Создаем экземпляр Dispatcher
# Dispatcher управляет обработкой всех событий бота: команды, сообщения, кнопки
dp = Dispatcher()

# Создаем объект бота
# В реальном проекте можно передать DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN)

# Создаем брокер RabbitMQ для работы с очередями сообщений
broker = RabbitBroker()

# -------------------------------
# Подписчик на очередь RabbitMQ
# -------------------------------

@broker.subscriber('orders')
async def handle_orders_and_send_message(data: str):
    """
    Функция-подписчик на очередь 'orders'.
    Когда в очередь приходит сообщение, бот отправляет его в Telegram.

    Параметры:
    - data (str): текст сообщения из очереди RabbitMQ
    """
    await bot.send_message(
        chat_id=926378677,  # ID чата, куда бот отправляет сообщение
        text=data           # Текст сообщения
    )

# -------------------------------
# Пример обработчика сообщений от пользователей (пока закомментирован)
# -------------------------------
# @dp.message()
# async def handle_message(msg: Message):
#     """
#     Простейший обработчик сообщений от пользователей.
#     Отправляет обратно ID чата пользователя.
#     """
#     await msg.answer(f"ID Вашего чата: {msg.chat.id}")

# -------------------------------
# Основная асинхронная функция запуска бота
# -------------------------------

async def main() -> None:
    """
    Запускает Telegram бота и Dispatcher.
    Dispatcher начинает polling и слушает все события.

    Дополнительно:
    - Асинхронно запускается RabbitBroker
    - После выхода из блока async with брокер корректно закрывается
    """
    # Контекстный менеджер async with автоматически вызывает broker.__aenter__ и broker.__aexit__
    # Это гарантирует, что соединение с RabbitMQ будет корректно открыто и закрыто
    async with broker:
        # Явный запуск брокера (может быть нужен для инициализации внутренних очередей и подключений)
        await broker.start()
        logging.info("Broker успешно запущен")

        # Запуск Telegram бота и диспетчера
        # dp.start_polling слушает все события бота (сообщения, команды)
        await dp.start_polling(bot)

    # Когда блок async with завершён, broker.__aexit__ автоматически закрывает соединение
    logging.info("Broker успешно прекратил свою работу")

# Точка входа скрипта
# -------------------------------

if __name__ == "__main__":
    # Настраиваем логирование в консоль с уровнем INFO
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Запускаем асинхронную функцию main через asyncio
    asyncio.run(main())
