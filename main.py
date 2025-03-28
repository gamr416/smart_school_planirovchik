import telebot

from random import randint
from datetime import datetime as dt
from database import *
from telebot import types


TOKEN = '8021686178:AAGmze85r7PUbYUw0jZRtqEEf3vGueP2NVI'
bot = telebot.TeleBot(TOKEN)

LOG = None

but_exit = types.InlineKeyboardButton('отмена', callback_data='отмена')

keyboard_home = types.InlineKeyboardMarkup()
but_add_task= types.InlineKeyboardButton('добавить задачу', callback_data='добавить задачу')
but_del_task= types.InlineKeyboardButton('удалить задачу', callback_data='удалить задачу')
but_check_tasks= types.InlineKeyboardButton('просмотреть задачи', callback_data='просмотреть задачи')
keyboard_home.add(but_add_task, but_check_tasks, but_del_task, but_exit)

keyboard_subjects = types.InlineKeyboardMarkup()
but_homework= types.InlineKeyboardButton('домашка', callback_data='домашка')
but_clubs= types.InlineKeyboardButton('кружки', callback_data='кружки')
but_personal= types.InlineKeyboardButton('личное', callback_data='личное')
keyboard_subjects.add(but_homework, but_clubs, but_personal, but_exit)

keyboard_add_subjects = types.InlineKeyboardMarkup()
but_add_homework= types.InlineKeyboardButton('домашка добавить', callback_data='домашка добавить')
but_add_clubs= types.InlineKeyboardButton('кружки добавить', callback_data='кружки добавить')
but_add_personal= types.InlineKeyboardButton('личное добавить', callback_data='личное добавить')
keyboard_add_subjects.add(but_add_homework, but_add_clubs, but_add_personal, but_exit)

keyboard_del_subjects = types.InlineKeyboardMarkup()
but_del_homework= types.InlineKeyboardButton('домашка удалить', callback_data='домашка удалить')
but_del_clubs= types.InlineKeyboardButton('кружки удалить', callback_data='кружки удалить')
but_del_personal= types.InlineKeyboardButton('личное удалить', callback_data='личное удалить')
keyboard_del_subjects.add(but_del_homework, but_del_clubs, but_del_personal, but_exit)



@bot.message_handler(commands=['start'])
def getting_started(message):
    bot.send_message(message.from_user.id, answer:="Скорее всего вы успешно зарегестрировались", reply_markup=keyboard_home)
    register_new_user(message.chat.id)

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')

@bot.message_handler(commands=['help'])
def getting_started1(message):
    bot.send_message(message.from_user.id, answer:="ок", reply_markup=keyboard_home)

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global echo
    global LOG
    global answer
    answer = ''
    if message.text == "добавить задачу":  
        bot.register_next_step_handler(bot.send_message(message.chat.id, answer:='Какая категория',
                                       reply_markup=keyboard_subjects), add_task_date)

    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {message.from_user.username}: {message.text} - {answer}\n')


@bot.callback_query_handler(func=lambda call: True)
def main_callback(call):    
    answer = ''
    print(call.data)
    if call.data == "отмена":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Иди нахуй', reply_markup=keyboard_home)
    
    if call.data == "добавить задачу":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Какая категория?', reply_markup=keyboard_add_subjects)

    if call.data == "удалить задачу":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Какая категория?', reply_markup=keyboard_del_subjects)
    
    if call.data == "просмотреть задачи":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Какая категория?', reply_markup=keyboard_subjects)

    if call.data == "домашка добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Дата и время()', )
    
    if call.data == "кружки добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Какая категория?', )
    
    if call.data == "личное добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Какая категория?', )
    

    if call.data == "домашка":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'домашка')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из домашки', reply_markup=keyboard)

    if call.data == "кружки":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'кружки')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из кружков', reply_markup=keyboard)

    if call.data == "личное":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'личное')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из личного', reply_markup=keyboard)


    if call.data == "домашка удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'домашка')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data == "кружки удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'кружки')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data == "личное удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard(call.message.chat.id, 'личное')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data in [''.join(i) + ' - удалить' for i in get_all_tasks(call.message.chat.id)]:
        print('УРА')


    LOG = open('log.txt', 'a')
    LOG.write(f'{dt.now().strftime("%d.%m.%Y %H:%M:%S")}: {call.message.from_user.username}: {call.message.text} - {answer}\n')



def add_task_date(message):
    try:
        time_and_date = message.text.split(' ')
        print(time_and_date)
    except: pass

def get_keyboard(user_id, tag):
    keyboard_tasks = types.InlineKeyboardMarkup()
    buttons_tasks = [types.InlineKeyboardButton(f'{i[3]}\n{i[2]}', callback_data=f'{i[3]}\n{i[2]}') for i in get_tagged_tasks(user_id, tag)]
    keyboard_tasks.add(but_exit)
    for button in buttons_tasks:
        keyboard_tasks.add(button)
    return keyboard_tasks

def get_keyboard_for_del(user_id, tag):
    keyboard_tasks = types.InlineKeyboardMarkup()
    buttons_tasks = [types.InlineKeyboardButton(f'{i[3]}\n{time[2]} - удалить', callback_data=f'{i[3]}\n{time[2]} - удалить') for i in get_tagged_tasks(user_id, tag)]
    keyboard_tasks.add(but_exit)
    for button in buttons_tasks:
        keyboard_task.add(button)
    return keyboard_tasks





bot.infinity_polling()