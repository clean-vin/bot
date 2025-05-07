from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from bot import dp  # должен экспортировать Dispatcher из bot.py

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.bot = bot  # привязываем бота к диспетчеру
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    webhook_url = "https://your-app-name.onrender.com/webhook"
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(webhook_url)

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
