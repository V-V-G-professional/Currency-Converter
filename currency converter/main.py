from tokens import bot
from currency_converter import CurrencyConverter
from telebot import types

currency = CurrencyConverter()
amount = 0


def couples():
    btn1 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
    btn2 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
    btn3 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
    btn4 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
    btn5 = types.InlineKeyboardButton('Другое значение', callback_data='else')
    return btn1, btn2, btn3, btn4, btn5


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите нужную сумму для конвертации.')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму.\nНапример: 100')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(*couples())
        bot.send_message(message.chat.id, 'Выбирите валютную пару', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть 0 или более.\nВпишите сумму.\nНапример: 100')
        bot.register_next_step_handler(message, summa)
        return

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}{values[1]}.\nМожете заново вписать сумму.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш.')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}{values[1]}.\nМожете заново вписать сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то пошло не так.\nВпишите значение заново.')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)
