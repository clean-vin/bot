import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

# Получаем токен из переменных окружения (настроить в Render → Environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)
dp = Dispatcher()

# Инициализация FastAPI
app = FastAPI()

# Роутинг вебхука
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}

# Пример простого хендлера на сообщение
@dp.message()
async def handle_message(message):
    await message.answer("Привет! Я работаю через вебхук на Render 😊")

# Настройка запуска (необязательно на Render, но полезно локально)
@app.on_event("startup")
async def on_startup():
    print("🚀 Bot is running")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
