# -*- coding: utf-8 -*-
import telebot
from config import TOKEN
from chat_logic import chating, begining


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_info(message):
    chat_id = message.from_user.id
    bot.send_message(chat_id, 'Доров, выбери свою группу', reply_markup=begining())


@bot.message_handler(content_types=['text'])
def get_text_mess(message):
    chat_id = message.from_user.id
    answer = chating(chat_id, message.text)
    print(answer)
    bot.send_message(chat_id, answer[0], reply_markup= answer[1])


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(e)
    pass