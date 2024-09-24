from telebot import types
import sqlite3
from loader import bot
from config_data import config
import requests
import json


def get_sales(message):
    # querystring['city'] = message.text.title()
    try:
        response = requests.get(config.url, headers=config.headers, params=config.querystring)
    except requests.ConnectionError as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка API, попробуйте позже')
    bot.send_message(message.chat.id, 'Результаты на основе введенных данных', reply_markup=types.ReplyKeyboardRemove())
    data = json.loads(response.text)
    listings = data.get('listings')
    if len(listings) == 0:
        bot.send_message(message.chat.id, 'Упс. Ничего не нашлось')
    else:
        s_id = 0
        for i in listings:
            s_id += 1
            address = i.get('address')
            web_url = i.get('rdc_web_url')
            history_lst = [s_id, config.querystring['city'], address, web_url]
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS history (id, city, address, url)""")
                conn.commit()
                cursor.execute("""INSERT INTO history VALUES (?, ?, ?, ?);""", history_lst)
            bot.send_message(message.chat.id, f'Адрес: {address}\nСсылка: {web_url}')
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='да', callback_data='yes')
    kb.add(btn)
    bot.send_message(message.chat.id, 'Вернуться в начало?', reply_markup=kb)
