from telebot import types

from loader import bot


@bot.message_handler(commands=['start', 'да'])  # Приветственное сообщение и вариант выбора поиск или история
@bot.callback_query_handler(func=lambda callback: callback.data == 'yes')
def send_welcome(data):
    kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Искать', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='История', callback_data='btn2')
    kb.add(btn1, btn2)
    if isinstance(data, types.Message):
        i = data.chat.id
    if isinstance(data, types.CallbackQuery):
        i = data.message.chat.id
    bot.send_message(i, "Привет. Я бот по поиску дома твоей мечты. Будем искать дом или посмотрим историю поиска?.",
                     reply_markup=kb)
