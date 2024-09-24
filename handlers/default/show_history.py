from telebot import types
import sqlite3
from loader import bot


@bot.callback_query_handler(func=lambda callback: callback.data == 'btn2')
def show_history(callback):
    # bot.send_message(message.chat.id, 'А зачем нам эта история? Ищи заново')
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM history ORDER BY id DESC LIMIT 10')
        data = cursor.fetchall()
    print(data)
    for i in data:
        city = i[1]
        address = i[2]
        web_url = i[3]
        bot.send_message(callback.message.chat.id, f'Город: {city}\nАдрес: {address}\nСсылка: {web_url}')
    kb = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton(text='да', callback_data='yes')
    kb.add(yes_btn)
    #kb = types.ReplyKeyboardMarkup()
    #btn = types.KeyboardButton(text='/да')
    #kb.add(btn)
    bot.send_message(callback.message.chat.id, 'Вернуться в начало?', reply_markup=kb)
