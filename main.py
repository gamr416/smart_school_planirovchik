import telebot

from random import randint
from datetime import datetime as dt
from database import *
from telebot import types



TOKEN = '8021686178:AAGmze85r7PUbYUw0jZRtqEEf3vGueP2NVI'
bot = telebot.TeleBot(TOKEN)

LOG = None

but_exit = types.InlineKeyboardButton('отмена', callback_data="отмена")

keyboard_home = types.InlineKeyboardMarkup()

keyboard_subjects = types.InlineKeyboardMarkup()

but_add_task= types.InlineKeyboardButton('добавить задачу', callback_data="добавить задачу")
but_del_task= types.InlineKeyboardButton('удалить задачу', callback_data="удалить задачу")
but_check_tasks= types.InlineKeyboardButton('просмотреть задачи', callback_data="просмотреть задачи")
keyboard_home.add(but_add_task, but_check_tasks, but_del_task, but_exit)

but_homework= types.InlineKeyboardButton('домашка', callback_data="домашка")
but_clubs= types.InlineKeyboardButton('кружки', callback_data="кружки")
but_personal= types.InlineKeyboardButton('личное', callback_data="личное")
keyboard_subjects.add(but_homework, but_clubs, but_personal, but_exit)


@bot.message_handler(commands=['start', 'help'])
def getting_started(message):
    bot.send_message(message.from_user.id, answer:="Скорее всего вы успешно зарегестрировались", reply_markup=keyboard_home)
    register_new_user(message.chat.id)

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global echo
    global LOG
    global answer
    answer = ''
    if message.text == "добавить задачу":  
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Какая категория',
                                       reply_markup=keyboard_subjects), add_task_date)

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.callback_query_handler(func=lambda call: True)
def main_callback(call):    
    if call.data == "отмена":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Иди нахуй', reply_markup=keyboard_home)
    
    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {call.message.from_user.username}: {call.message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def add_task_date(message):
    try:
        time_and_date = message.text.split(' ')
        print(time_and_date)
    except: pass


bot.infinity_polling()