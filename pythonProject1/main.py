from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
import logging

# Вставьте сюда ваш токен Telegram-бота
API_TOKEN = 'Your token'


logging.basicConfig(level=logging.INFO)

# Создание экземпляров бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


with open('book.txt', 'r', encoding='utf-8') as f:
    book_text = f.read()

words = book_text.split()
pages = [" ".join(words[i:i + 100]) for i in range(0, len(words), 100)]
total_pages = len(pages)

def create_keyboard(current_page: int):
    prev_btn = InlineKeyboardButton(
        text='Назад',
        callback_data=f'prev_{current_page}'
    )
    next_btn = InlineKeyboardButton(
        text='Вперед',
        callback_data=f'next_{current_page}'
    )
    num_pages_btn = InlineKeyboardButton(
        text=f"Страница {current_page + 1}/{total_pages}",
        callback_data='page_info'
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[prev_btn, next_btn], [num_pages_btn]])
    return keyboard

@dp.message(Command(commands='beginning'))
async def process_start_command(message: Message):
    current_page = 0
    await message.answer(
        text=pages[current_page],
        reply_markup=create_keyboard(current_page)
    )


@dp.callback_query(F.data.startswith('prev_'))
async def process_prev_button(callback: CallbackQuery):
    current_page = int(callback.data.split('_')[1])
    if current_page > 0:
        current_page -= 1
        await callback.message.edit_text(
            text=pages[current_page],
            reply_markup=create_keyboard(current_page)
        )
    await callback.answer()

@dp.callback_query(F.data.startswith('next_'))
async def process_next_button(callback: CallbackQuery):
    current_page = int(callback.data.split('_')[1])
    if current_page < total_pages - 1:
        current_page += 1
        await callback.message.edit_text(
            text=pages[current_page],
            reply_markup=create_keyboard(current_page)
        )
    await callback.answer()

# Обработка команды /start
@dp.message(Command(commands='start'))
async def send_welcome(message: types.Message):
    await message.reply("""
Привет читатель! 
Это бот, в котором ты можешь почитать книгу Рэя Бредбери "Марсианские Хроники". 
Чтобы узнать о командах бота, введи /help
""")

# Обработка команды /help
@dp.message(Command(commands='help'))
async def send_help(message: types.Message):
    await message.reply("""
Доступные команды:
/start - Начать взаимодействие с ботом
/help - Получить справку
/beginning - Начать читать книгу
/continue - Продолжить читать с того места, где остановились
/bookmarks - Посмотреть закладки
""")

# Обработка команды /continue
@dp.message(Command(commands='continue'))
async def send_continue(message: types.Message):
    # Для упрощения продолжаем с первой страницы
    current_page = 0
    await message.answer(
        text=pages[current_page],
        reply_markup=create_keyboard(current_page)
    )

# Обработка команды /bookmarks (заглушка)
@dp.message(Command(commands='bookmarks'))
async def send_bookmarks(message: types.Message):
    await message.reply("Закладки пока не реализованы.")

# Установка команд бота
async def set_commands():
    commands = [
        BotCommand(command="/start", description="Начать взаимодействие с ботом"),
        BotCommand(command="/help", description="Получить справку"),
        BotCommand(command="/beginning", description="Начать читать"),
        BotCommand(command="/continue", description="Продолжить читать"),
        BotCommand(command="/bookmarks", description="Посмотреть закладки")
    ]
    await bot.set_my_commands(commands)

dp.run_polling(bot)
