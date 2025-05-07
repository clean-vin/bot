import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

# Получаем токен и URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-app-name.onrender.com/webhook

# Инициализация бота и диспетчера
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)
dp = Dispatcher()

# FastAPI приложение
app = FastAPI()

# Роут для Telegram вебхука
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}

# Простой обработчик
@dp.message()
async def handle_message(message):
    await message.answer("Привет с Render! 🚀")

# Устанавливаем вебхук при запуске
@app.on_event("startup")
async def on_startup():
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Вебхук установлен: {WEBHOOK_URL}")
    else:
        print("⚠️ WEBHOOK_URL не задан")
    print("🚀 Bot is running")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
