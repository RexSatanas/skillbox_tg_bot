from loader import bot
import handlers




#bot = telebot.TeleBot(BOT_TOKEN)

""""
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


# выбор типа поиска /low - дешевле, /high -  дороже, /custom - кастом настройки
@bot.callback_query_handler(func=lambda callback: callback.data == 'btn1')
def main_menu(callback):
    if callback.data == 'btn1':
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""'''DELETE FROM history'''""")
            conn.commit()
        send = bot.send_message(callback.message.chat.id, 'Введите код города: ')
        bot.register_next_step_handler(send, message_city_names)


def message_city_names(message):
    querystring['state_code'] = message.text.upper()
    send = bot.send_message(message.chat.id, 'Введите название города: ')
    bot.register_next_step_handler(send, type_of_search)


def type_of_search(message):
    querystring['city'] = message.text.title()
    kb = types.InlineKeyboardMarkup(row_width=2)
    low = types.InlineKeyboardButton(text='Дешевле', callback_data='low')
    high = types.InlineKeyboardButton(text='Дороже', callback_data='high')
    custom = types.InlineKeyboardButton(text='По цене', callback_data='custom')
    kb.add(low, high, custom)
    bot.send_message(message.chat.id, 'Какой дом будем искать?', reply_markup=kb)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'low' or callback.data == 'high' or callback.data == 'custom')
def choose_search(callback):
    if callback.data == 'low':
        querystring['sort'] = 'price_low'
        get_sales(callback.message)
    elif callback.data == 'high':
        querystring['sort'] = 'price_high'
        get_sales(callback.message)
    elif callback.data == 'custom':
        send = bot.send_message(callback.message.chat.id, 'Введите минимальную цену в долларах: ',
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(send, set_min_price)


def set_min_price(message):
    querystring['price_min'] = message.text
    querystring['sort'] = 'relevance'
    send = bot.send_message(message.chat.id, 'Введите максимальную цену в долларах: ')
    bot.register_next_step_handler(send, set_max_price)


def set_max_price(message):
    querystring['price_max'] = message.text
    get_sales(message)


def get_sales(message):
    # querystring['city'] = message.text.title()
    try:
        response = requests.get(url, headers=headers, params=querystring)
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
            history_lst = [s_id, querystring['city'], address, web_url]
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""'''CREATE TABLE IF NOT EXISTS history (id, city, address, url)'''""")
                conn.commit()
                cursor.execute("""'''INSERT INTO history VALUES (?, ?, ?, ?)'''""", history_lst)
            bot.send_message(message.chat.id, f'Адрес: {address}\nСсылка: {web_url}')
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='да', callback_data='yes')
    kb.add(btn)
    bot.send_message(message.chat.id, 'Вернуться в начало?', reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: callback.data == 'btn2')
def show_history(message):
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
        bot.send_message(message.chat.id, f'Город: {city}\nАдрес: {address}\nСсылка: {web_url}')
    kb = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton(text='/да')
    kb.add(btn)
    bot.send_message(message.chat.id, 'Вернуться в начало?', reply_markup=kb)
"""

if __name__ == '__main__':

    bot.infinity_polling()
