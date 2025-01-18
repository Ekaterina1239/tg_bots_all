# Настройки
import pymysql
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN ='7642998085:AAGWDelrBVrQ5KnlidwD9v2czkpxDDzE7r8'
DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "baza"

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для подключения к базе данных
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

# Хэндлер для команды "/start"
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Проверка, существует ли пользователь
        cursor.execute("SELECT * FROM category")
        category = cursor.fetchall()



    # Добавляем кнопки из category
        kb_builder = ReplyKeyboardBuilder()

        buttons: list[KeyboardButton] = [
            KeyboardButton(text=i['title']) for i in category
        ]
        kb_builder.row(*buttons)
        await message.answer(
            text='Вот такая получается клавиатура',
            reply_markup=kb_builder.as_markup()
        )


@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Получаем данные из категории
        cursor.execute("SELECT * FROM category")
        category = cursor.fetchall()

    # Создаем инлайн-клавиатуру
    keyboard = InlineKeyboardMarkup()
    for i in category:
        keyboard.add(InlineKeyboardButton(text=i['title'], callback_data=f"category_{i['id']}"))

    await message.answer(
        text='Вот такая получается клавиатура',
        reply_markup=keyboard
    )

@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Получаем данные из категории
        cursor.execute("SELECT * FROM category")
        category = cursor.fetchall()

    # Создаем инлайн-кнопки из категории
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=i['title'], callback_data=f"category_{i['id']}") for i in category]
    kb_builder.row(*buttons)

    await message.answer(
        text='Вот такая получается клавиатура',
        reply_markup=kb_builder.as_markup()
    )


dp.run_polling(bot)