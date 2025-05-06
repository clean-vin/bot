from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    if lang == "ru":
        buttons = [
            [KeyboardButton(text="🔍 Проверить VIN")],
            [KeyboardButton(text="🗑 Удалить VIN")],
            [KeyboardButton(text="📘 Как это работает")],
            [KeyboardButton(text="💳 Способы оплаты")],
            [KeyboardButton(text="👨‍💼 Связаться с менеджером")]
        ]
    else:
        buttons = [
            [KeyboardButton(text="🔍 Check VIN")],
            [KeyboardButton(text="🗑 Delete VIN")],
            [KeyboardButton(text="📘 How it works")],
            [KeyboardButton(text="💳 Payment Methods")],
            [KeyboardButton(text="👨‍💼 Contact Manager")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_after_payment_menu(lang: str) -> ReplyKeyboardMarkup:
    if lang == "ru":
        buttons = [
            [KeyboardButton(text="🔁 Проверить еще один VIN"), KeyboardButton(text="⏳ Проверить статус удаления")]
        ]
    else:
        buttons = [
            [KeyboardButton(text="🔁 Check another VIN"), KeyboardButton(text="⏳ Check removal status")]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

payment_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Visa/Mastercard")],
        [KeyboardButton(text="₿ Crypto")],
        [KeyboardButton(text="💰 PayPal")]
    ],
    resize_keyboard=True
)
