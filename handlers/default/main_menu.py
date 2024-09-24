from telebot import types
import sqlite3
from loader import bot
from config_data import config


@bot.callback_query_handler(func=lambda callback: callback.data == 'btn1')
def message_city_codes(callback):
    if callback.data == 'btn1':
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM history""")
            conn.commit()
        send = bot.send_message(callback.message.chat.id, 'Введите код города: ')
        bot.register_next_step_handler(send, message_city_names)


def message_city_names(message):
    config.querystring['state_code'] = message.text.upper()
    send = bot.send_message(message.chat.id, 'Введите название города: ')
    bot.register_next_step_handler(send, type_of_search)


def type_of_search(message):
    config.querystring['city'] = message.text.title()
    kb = types.InlineKeyboardMarkup(row_width=2)
    low = types.InlineKeyboardButton(text='Дешевле', callback_data='low')
    high = types.InlineKeyboardButton(text='Дороже', callback_data='high')
    custom = types.InlineKeyboardButton(text='По цене', callback_data='custom')
    kb.add(low, high, custom)
    bot.send_message(message.chat.id, 'Какой дом будем искать?', reply_markup=kb)
