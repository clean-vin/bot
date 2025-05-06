import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, MANAGER_CHAT_ID, PAYPAL_LINK, CRYPTO_WALLET
from aiogram.client.default import DefaultBotProperties


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


# Состояния
class UserState(StatesGroup):
    choosing_language = State()
    waiting_for_vin = State()
    deleting_vin = State()
    waiting_for_payment = State()


user_language = {}


# Кнопки
language_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇸 English")]
    ],
    resize_keyboard=True
)


menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Проверить VIN")],
        [KeyboardButton(text="❌ Удалить VIN")],
        [KeyboardButton(text="💳 Способы оплаты")],
        [KeyboardButton(text="ℹ️ Как это работает"), KeyboardButton(text="📞 Связаться с менеджером")]
    ],
    resize_keyboard=True
)


menu_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Check VIN")],
        [KeyboardButton(text="❌ Delete VIN")],
        [KeyboardButton(text="💳 Payment Methods")],
        [KeyboardButton(text="ℹ️ How it works"), KeyboardButton(text="📞 Contact Manager")]
    ],
    resize_keyboard=True
)


def get_menu(lang):
    return menu_ru if lang == "ru" else menu_en


def vin_result_kb(lang):
    if lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔁 Проверить ещё один VIN")],
                [KeyboardButton(text="❌ Удалить историю VIN")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔁 Check another VIN")],
                [KeyboardButton(text="❌ Delete VIN history")]
            ],
            resize_keyboard=True
        )


def payment_kb(lang):
    if lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💳 Visa/Mastercard")],
                [KeyboardButton(text="💰 PayPal")],
                [KeyboardButton(text="🪙 Криптовалюта")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💳 Visa/Mastercard")],
                [KeyboardButton(text="💰 PayPal")],
                [KeyboardButton(text="🪙 Cryptocurrency")]
            ],
            resize_keyboard=True
        )


# Старт
@dp.message(F.text.in_({"/start", "start"}))
async def start(message: Message, state: FSMContext):
    await message.answer("🇷🇺 Пожалуйста, выберите язык / 🇺🇸 Please select language:", reply_markup=language_kb)
    await state.set_state(UserState.choosing_language)


@dp.message(UserState.choosing_language)
async def set_language(message: Message, state: FSMContext):
    text = message.text
    if text == "🇷🇺 Русский":
        user_language[message.from_user.id] = "ru"
        await message.answer("Главное меню:", reply_markup=menu_ru)
    elif text == "🇺🇸 English":
        user_language[message.from_user.id] = "en"
        await message.answer("Main menu:", reply_markup=menu_en)
    await state.clear()


# Проверка VIN
@dp.message(F.text.in_({"🔍 Проверить VIN", "🔍 Check VIN"}))
async def ask_vin(message: Message, state: FSMContext):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer("Введите 17-значный VIN код:" if lang == "ru" else "Enter the 17-character VIN code:")
    await state.set_state(UserState.waiting_for_vin)


@dp.message(UserState.waiting_for_vin)
async def show_vin_report(message: Message, state: FSMContext):
    vin = message.text.upper()
    lang = user_language.get(message.from_user.id, "ru")
    description_ru = [
        "Toyota Camry 2017, удар в переднюю часть",
        "BMW X5 2019, боковое столкновение",
        "Ford Mustang 2020, без повреждений"
    ]
    description_en = [
        "Toyota Camry 2017, front-end damage",
        "BMW X5 2019, side collision",
        "Ford Mustang 2020, no damage"
    ]
    description = random.choice(description_ru if lang == "ru" else description_en)
    report = f"<b>VIN:</b> {vin}\n<b>История:</b> {description}\n<b>Стоимость удаления:</b> $30" if lang == "ru" else \
             f"<b>VIN:</b> {vin}\n<b>History:</b> {description}\n<b>Removal cost:</b> $30"
    await message.answer(report, reply_markup=vin_result_kb(lang))
    await state.clear()


# Повторная проверка VIN
@dp.message(F.text.in_({"🔁 Проверить ещё один VIN", "🔁 Check another VIN"}))
async def repeat_vin_check(message: Message, state: FSMContext):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer("Введите 17-значный VIN код:" if lang == "ru" else "Enter the 17-character VIN code:")
    await state.set_state(UserState.waiting_for_vin)


# Удаление VIN
@dp.message(F.text.in_({"❌ Удалить VIN", "❌ Delete VIN", "❌ Удалить историю VIN", "❌ Delete VIN history"}))
async def ask_delete_vin(message: Message, state: FSMContext):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer("Введите VIN, который вы хотите удалить:" if lang == "ru" else "Enter the VIN you want to delete:")
    await state.set_state(UserState.deleting_vin)


@dp.message(UserState.deleting_vin)
async def handle_delete_vin(message: Message, state: FSMContext):
    vin = message.text.upper()
    lang = user_language.get(message.from_user.id, "ru")
    description_ru = [
        "Toyota Camry 2017, удар в переднюю часть",
        "BMW X5 2019, боковое столкновение",
        "Ford Mustang 2020, без повреждений"
    ]
    description_en = [
        "Toyota Camry 2017, front-end damage",
        "BMW X5 2019, side collision",
        "Ford Mustang 2020, no damage"
    ]
    description = random.choice(description_ru if lang == "ru" else description_en)
    report = f"<b>VIN:</b> {vin}\n<b>История:</b> {description}\n<b>Стоимость удаления:</b> $30" if lang == "ru" else \
             f"<b>VIN:</b> {vin}\n<b>History:</b> {description}\n<b>Removal cost:</b> $30"
    await message.answer(report)
    await message.answer("Выберите способ оплаты:" if lang == "ru" else "Choose a payment method:", reply_markup=payment_kb(lang))
    await state.update_data(vin=vin)
    await state.set_state(UserState.waiting_for_payment)


# Способы оплаты
@dp.message(F.text.in_({"💳 Способы оплаты", "💳 Payment Methods"}))
async def payment_methods(message: Message):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer("Выберите способ оплаты:" if lang == "ru" else "Choose a payment method:", reply_markup=payment_kb(lang))


# Оплата
@dp.message(F.text.in_({"💳 Visa/Mastercard", "💰 PayPal"}))
async def pay_with_paypal(message: Message, state: FSMContext):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer(
        f"{'Оплатите по ссылке:' if lang == 'ru' else 'Pay via link:'}\n{PAYPAL_LINK}\n\n"
        f"{'Пожалуйста, прикрепите фото чека после оплаты.' if lang == 'ru' else 'Please attach a photo of the receipt after payment.'}"
    )
    await state.set_state(UserState.waiting_for_payment)


@dp.message(F.text.in_({"🪙 Криптовалюта", "🪙 Cryptocurrency"}))
async def crypto(message: Message, state: FSMContext):
    lang = user_language.get(message.from_user.id, "ru")
    await message.answer(
        f"{'Отправьте $30 на кошелек:' if lang == 'ru' else 'Send $30 to the wallet:'}\n"
        f"<code>{CRYPTO_WALLET}</code>\n\n"
        f"{'После оплаты прикрепите фото чека.' if lang == 'ru' else 'After payment, attach a receipt photo.'}"
    )
    await state.set_state(UserState.waiting_for_payment)


@dp.message(F.photo, UserState.waiting_for_payment)
async def receive_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    vin = data.get("vin", "не указан")
    user = message.from_user
    caption = f"📥 Новый чек об оплате\n👤 Пользователь: @{user.username} ({user.full_name})\nVIN: {vin}"
    await bot.send_photo(chat_id=MANAGER_CHAT_ID, photo=message.photo[-1].file_id, caption=caption)


    lang = user_language.get(message.from_user.id, "ru")
    await message.answer(
        "Чек получен, спасибо! Менеджер свяжется с вами в течение 24 часов." if lang == "ru"
        else "Receipt received, thank you! The manager will contact you within 24 hours.",
        reply_markup=get_menu(lang)
    )
    await state.clear()


# Менеджер и инструкция
@dp.message(F.text.in_({"📞 Связаться с менеджером", "📞 Contact Manager"}))
async def contact_manager(message: Message):
    lang = user_language.get(message.from_user.id, "ru")
    text = (
         " Нажмите, чтобы связаться с менеджером: @rm_vin\n"
          if lang == "ru" else
          " Please contact support assistant: @rm_vin\n"
          )
    await message.answer(text)

@dp.message(F.text.in_({"ℹ️ Как это работает", "ℹ️ How it works"}))
async def how_it_works(message: Message):
    lang = user_language.get(message.from_user.id, "ru")
    text = (
        "🚗 <b>Введите VIN вашего авто</b>\n"
        "📄 <b>Получите полный аукционный отчет</b>\n"
        "💳 <b>Выберите способ оплаты и оплатите удаление VIN</b>\n"
        "⏱️ <b>Через 24 часа история VIN будет очищена</b>"
        if lang == "ru" else
        "🚗 <b>Enter your car VIN</b>\n"
        "📄 <b>Get full auction report</b>\n"
        "💳 <b>Select payment type and confirm VIN removal</b>\n"
        "⏱️ <b>Within 24 hours, unwanted info will be deleted</b>"
    )
    await message.answer(text)


# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))