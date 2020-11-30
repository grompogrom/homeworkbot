# -*- coding: utf-8 -*-
import telebot
from config import TOKEN
from chat_logic import chating, begining, again_registation


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_info(message):
    chat_id = message.from_user.id
    begin_info = begining(chat_id)
    bot.send_message(chat_id, begin_info[0], reply_markup=begin_info[1])


@bot.message_handler(content_types=['text'])
def get_text_mess(message):
    chat_id = message.from_user.id
    answer = chating(chat_id, message.text)
    print(answer)
    if len(answer) == 3:
        bot.send_message(chat_id, answer[0], reply_markup=answer[1], )
    else:
        bot.send_message(chat_id, answer[0], reply_markup= answer[1])


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = ''
    chat_id = call.from_user.id
    if call.data == 'cb_rereg':
        answer = again_registation(chat_id)
    elif call.data == 'cb_history':
        answer = '(Архив дз) Функция пока в разработке'
    elif call.data == 'cb_feedback':
        answer = '(Отзыв) Функция пока в разработке'
    bot.send_message(chat_id, answer[0], reply_markup=answer[1])


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(e)
    pass