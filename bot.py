import telebot
import requests
from telebot import types
from config import *

curr1 = "RUB"
curr2 = "USD"

currs = ["USD", "EUR", "RUB", "BTC"]


def get_rate(currancy1, currancy2):
    key = currancy1 + "_" + currancy2
    result = requests.get(url + "q=" + key + "&compact=ultra&apiKey=" + api_key).json()
    return result[key]


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def input_curr1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    row = [types.KeyboardButton(c) for c in currs]
    markup.add(*row)

    msg = bot.send_message(message.chat.id, "\U0001F4B5 Выберите вашу валюту:", reply_markup=markup)
    bot.register_next_step_handler(msg, input_curr2)


def input_curr2(message):
    global curr1
    curr1 = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    row = [types.KeyboardButton(c) for c in currs if c != curr1]
    markup.add(*row)

    msg = bot.send_message(message.chat.id, "\U0001F4B6 В какую хотите перевести?", reply_markup=markup)
    bot.register_next_step_handler(msg, input_amount)


def input_amount(message):
    global curr2
    curr2 = message.text
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, f"\U0001F4B8 Сумма перевода из {curr1} в {curr2}:", reply_markup=markup)
    bot.register_next_step_handler(msg, calc)


def calc(message):
    try:
        rate = get_rate(curr1, curr2)
        count = float(message.text)
        amount = count * rate
        output = f"\U0001F4B0 {count:0,.2f} {curr1} = {amount:0,.2f} {curr2}"

        if curr1 == "BTC":
            output = f"\U0001F4B0 {count:.6f} {curr1} = {amount:0,.2f} {curr2}"

        if curr2 == "BTC":
            output = f"\U0001F4B0 {count:0,.2f} {curr1} = {amount:.6f} {curr2}"

        bot.send_message(message.chat.id, output)

    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка! Попробуйте еще /start")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
