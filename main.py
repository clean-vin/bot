import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp import web
from dotenv import load_dotenv

load_dotenv()  # если используешь .env файл

BOT_TOKEN = os.getenv("BOT_TOKEN")  # или напрямую строкой, если тестируешь

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Хендлер на сообщения
@dp.message(F.text)
async def handle_message(message: Message):
    await message.answer("Привет! Я работаю через webhook 🚀")


# Веб-сервер FastAPI (или AioHTTP здесь)
async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")  # пример: https://your-app-name.onrender.com/webhook
    await bot.set_webhook(webhook_url)


def create_app():
    app = web.Application()
    dp.startup.register(on_startup)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    return app


# Запуск приложения
if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8000)
