from telebot import types
from loader import bot
from config_data import config
from . import get_sales_f


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'low' or callback.data == 'high' or callback.data == 'custom')
def choose_search(callback):
    if callback.data == 'low':
        config.querystring['sort'] = 'price_low'
        get_sales_f.get_sales(callback.message)
    elif callback.data == 'high':
        config.querystring['sort'] = 'price_high'
        get_sales_f.get_sales(callback.message)
    elif callback.data == 'custom':
        send = bot.send_message(callback.message.chat.id, 'Введите минимальную цену в долларах: ',
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, set_min_price)


def set_min_price(message):
    config.querystring['price_min'] = message.text
    config.querystring['sort'] = 'relevance'
    send = bot.send_message(message.chat.id, 'Введите максимальную цену в долларах: ')
    bot.register_next_step_handler(send, set_max_price)


def set_max_price(message):
    config.querystring['price_max'] = message.text
    get_sales_f.get_sales(message)
