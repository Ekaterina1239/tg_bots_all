import pymysql
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Настройки
BOT_TOKEN = '7642998085:AAGWDelrBVrQ5KnlidwD9v2czkpxDDzE7r8'
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "user_database"

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для подключения к базе данных
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

# Хэндлер для команды "/start"
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    telegram_id = message.from_user.id
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка, существует ли пользователь
            cursor.execute("SELECT * FROM users WHERE my_id = %s", (telegram_id,))
            user = cursor.fetchone()
        if user:
            # Если пользователь найден
            await message.answer(f"Добро пожаловать, {user['name']}!")
        else:
            # Если пользователя нет
            await message.answer("Вы не зарегистрированы. Введите ваше имя для регистрации:")
    finally:
        connection.close()

# Хэндлер для регистрации пользователя
@dp.message()
async def process_registration_or_other(message: Message):
    telegram_id = message.from_user.id
    user_name = message.text.strip()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка, существует ли пользователь
            cursor.execute("SELECT * FROM users WHERE my_id = %s", (telegram_id,))
            user = cursor.fetchone()
            if not user:
                # Регистрация нового пользователя
                cursor.execute("INSERT INTO users (name, my_id, status) VALUES (%s, %s, %s)", (user_name, telegram_id, "active"))
                connection.commit()
                await message.answer("Регистрация успешно завершена! Добро пожаловать!")
            else:
                # Ответ на другие сообщения
                await message.answer("Вы уже зарегистрированы. Отправьте /start для начала.")
    finally:
        connection.close()

# Запуск бота
dp.run_polling(bot)