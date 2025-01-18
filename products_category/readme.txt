# Telegram Bot: Dynamic Category Keyboard

This repository contains a Telegram bot implementation that dynamically generates keyboards based on database content. It demonstrates key features such as:

- Integration with a MySQL database using `pymysql`.
- Dynamic creation of reply and inline keyboards.
- Handling `/start` command to display categories from the database.

---

## Features

- Fetches category data from a MySQL database.
- Creates dynamic keyboards:
  - **Reply Keyboard**: Displays categories as buttons.
  - **Inline Keyboard**: Buttons with callback data for further interactions.
- Demonstrates basic bot functionality using `aiogram`.

---

## Installation and Setup

### Requirements

- Python 3.8+
- Libraries:
  - `aiogram`
  - `pymysql`
- MySQL database with a `category` table.

### Steps to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/telegram-dynamic-keyboard-bot.git
   cd telegram-dynamic-keyboard-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Database**
   Update the database settings in the script:
   ```python
   DB_HOST = "localhost"
   DB_USER = "root"
   DB_NAME = "baza"
   ```
   Ensure your MySQL database contains a `category` table with `id` and `title` columns.

4. **Set Up the Bot Token**
   Replace the placeholder token in the script:
   ```python
   BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   ```

5. **Run the Bot**
   ```bash
   python bot.py
   ```

---

## Code Explanation

### Key Components

1. **Database Connection**
   ```python
   def get_connection():
       return pymysql.connect(
           host=DB_HOST,
           user=DB_USER,
           database=DB_NAME,
           charset="utf8mb4",
           cursorclass=pymysql.cursors.DictCursor
       )
   ```
   Establishes a connection to the MySQL database.

2. **Handling `/start` Command**

   - **Reply Keyboard Example**
     ```python
     @dp.message(Command(commands="start"))
     async def process_start_command(message: Message):
         connection = get_connection()
         with connection.cursor() as cursor:
             cursor.execute("SELECT * FROM category")
             category = cursor.fetchall()

         kb_builder = ReplyKeyboardBuilder()
         buttons = [KeyboardButton(text=i['title']) for i in category]
         kb_builder.row(*buttons)

         await message.answer(
             text='Вот такая получается клавиатура',
             reply_markup=kb_builder.as_markup()
         )
     ```

   - **Inline Keyboard Example**
     ```python
     @dp.message(Command(commands="start"))
     async def process_start_command(message: Message):
         connection = get_connection()
         with connection.cursor() as cursor:
             cursor.execute("SELECT * FROM category")
             category = cursor.fetchall()

         keyboard = InlineKeyboardMarkup()
         for i in category:
             keyboard.add(InlineKeyboardButton(text=i['title'], callback_data=f"category_{i['id']}"))

         await message.answer(
             text='Вот такая получается клавиатура',
             reply_markup=keyboard
         )
     ```

3. **Bot Polling**
   ```python
   dp.run_polling(bot)
   ```
   Starts the bot and listens for updates.

---

## Contribution

If you have improvements or additional features to suggest, feel free to:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed explanation of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
