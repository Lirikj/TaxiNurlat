from telebot import telebot, types
from datetime import datetime
import sqlite3

def init_db():
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        date_joined TEXT,
                        Number INTEGER, 
                        ban INTEGER DEFAULT 0
                )''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()


def user_exists(user_id):
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = c.fetchone()

        return user is not None  
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        if conn:
            conn.close()


def add_user_to_db(user_id, username, first_name, last_name, number):
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, username, first_name, last_name, date_joined, Number) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, username, first_name, last_name, 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"), number))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        if conn:
            conn.close()


bot = telebot.TeleBot('6423951514:AAE848xYBRpAx92gihFxrnWyXr70-ULgev0')


@bot.message_handler(commands=['start', 'st', 'mn', 'menu'])
def start_message(message):
    user = message.from_user
    user_id = message.from_user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ''
    username = message.from_user.username

    if user_exists(user_id): 
        markup = types.InlineKeyboardMarkup(row_width=1) 
        web_app = types.WebAppInfo("https://lirikj.github.io/webapp.github.io/") # ссылка на приложение 
        web_app_button = types.KeyboardButton('🚖Заказать такси🚖', web_app=web_app )
        markup.add(web_app_button)
        bot.send_message(message.chat.id, f'Привет, {first_name}'
                        '\nдля вызова такси перейди в приложение', reply_markup=markup)
    else: 
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        get_phone = types.KeyboardButton('📞Ваш номер', request_contact=True) 
        markup.add(get_phone)
        number = bot.send_message(message.chat.id, 
                                  '🚕Привет, я бот для заказа такси.\nЧтоб заказать такси мне нужен твой номер телефона, надеюсь ты не против?', 
                                  reply_markup=markup) 
        bot.register_next_step_handler(number, registration_user, user_id, username, first_name, last_name) 


def registration_user(message, user_id, username, first_name, last_name):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        add_user_to_db(user_id, username, first_name, last_name, phone_number)
        bot.send_message(message.chat.id, 'Спасибо! Ваш номер добавлен.')
    else:
        number = bot.send_message(message.chat.id, 'Ошибка: номер телефона не был передан.')
        bot.register_next_step_handler(number, registration_user, user_id, username, first_name, last_name) 


@bot.message_handler(commands=['info', 'developers']) 
def info(message):
    bot.send_message(message.chat.id, '👨🏼‍💻developer - @Lirikj'
                                    '\n🧑🏻‍💻developer - @NFCshka')


init_db()
bot.polling()