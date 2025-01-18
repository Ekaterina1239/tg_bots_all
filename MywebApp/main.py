
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, \
    MenuButtonWebApp, WebAppInfo

# Вставьте сюда ваш токен Telegram-бота
API_TOKEN = 'Your token'


# Создание экземпляров бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()



APP_BASE_URL = getenv("APP_BASE_URL")

@dp.message(Command(commands='start'))
async def cmd_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Order Food",
                    web_app=types.WebAppInfo(url="https://steepcoder.uz/mybots/test.html"),
                )
            ]
        ]
    )
    await message.answer("<b>Hey!</b>\nYou can order food here!", reply_markup=markup)


# @dp.message_handler(content_type=['web_app_data'])
# async def web_app(message: types.Message):
#     await message.answer(message.web_app_data.data)
@dp.message_handler(content_types="web_app_data")
async def enter_date(message: Message) -> None:
    message.answer("Test")
dp.run_polling(bot)
