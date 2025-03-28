import telebot
import os
import subprocess
import uuid
import speech_recognition as sr
import threading
import time

import datetime as dt
from database import *
from telebot import types
from ai import call_ai

TOKEN = '8021686178:AAGmze85r7PUbYUw0jZRtqEEf3vGueP2NVI'
bot = telebot.TeleBot(TOKEN)

LOG = None

but_exit = types.InlineKeyboardButton('отмена', callback_data='отмена')

keyboard_home = types.InlineKeyboardMarkup()
but_add_task= types.InlineKeyboardButton('добавить задачу', callback_data='добавить задачу')
but_del_task= types.InlineKeyboardButton('удалить задачу', callback_data='удалить задачу')
but_check_tasks= types.InlineKeyboardButton('просмотреть задачи', callback_data='просмотреть задачи')
but_ask_ai = types.InlineKeyboardButton('спросить ии', callback_data='спросить ии')
keyboard_home.add(but_add_task, but_check_tasks, but_del_task, but_ask_ai, but_exit)

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
    bot.send_message(message.from_user.id, answer:="Добро пожаловать в сервис для планирования школьных дел. Бот поддерживает голосовой ввод, возможность добавлять и удалять задачи, помечать их важными и распределять по категориям. По истечению срока на выполнение задачи, вам будет отправлено уведомление. Не пишите большие описания. Приятного пользования.", reply_markup=keyboard_home)
    register_new_user(message.chat.id)



@bot.message_handler(commands=['help'])
def getting_started1(message):
    bot.send_message(message.from_user.id, answer:="оБот поддерживает голосовой ввод, возможность добавлять и удалять задачи, помечать их важными и распределять по категориям.", reply_markup=keyboard_home)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global echo
    global LOG
    global answer
    answer = ''
    if message.text == "добавить задачу":  
        bot.register_next_step_handler(bot.send_message(message.chat.id, answer:='Какая категория',
                                       reply_markup=keyboard_subjects), add_task_date)




@bot.callback_query_handler(func=lambda call: True)
def main_callback(call):    
    answer = ''
    print(f'[{call.data}]')
    print([' '.join(i) + ' - удалить' for i in get_all_tasks(call.message.chat.id)])
    if call.data == "отмена":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, answer:='Отменено', reply_markup=keyboard_home)
        try:
            os.remove(f'newtask{call.message.chat.id}')
        except:
            pass
    
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
        f = open(f'newtask{call.message.chat.id}', 'a')
        f.write('домашка')
        f.close()
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, answer:='Дата и время(hh:mm dd.mm.yyyy)'), add_task_date)
    
    if call.data == "кружки добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        f = open(f'newtask{call.message.chat.id}', 'a')
        f.write('кружки')
        f.close()
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, answer:='Дата и время(hh:mm dd.mm.yyyy)'), add_task_date)

    if call.data == "личное добавить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        f = open(f'newtask{call.message.chat.id}', 'a')
        f.write('личное')
        f.close()
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, answer:='Дата и время(hh:mm dd.mm.yyyy)'), add_task_date)
    

    if call.data == "домашка":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_done(call.message.chat.id, 'домашка')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из домашки. Нажмите,чтобы пометить, как выполненную', reply_markup=keyboard)

    if call.data == "кружки":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_done(call.message.chat.id, 'кружки')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из кружков. Нажмите,чтобы пометить, как выполненную', reply_markup=keyboard)

    if call.data == "личное":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_done(call.message.chat.id, 'личное')
        bot.send_message(call.message.chat.id, answer:='Вот задачи из личного. Нажмите,чтобы пометить, как выполненную', reply_markup=keyboard)


    if call.data == "домашка удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_for_del(call.message.chat.id, 'домашка')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data == "кружки удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_for_del(call.message.chat.id, 'кружки')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data == "личное удалить":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = get_keyboard_for_del(call.message.chat.id, 'личное')
        bot.send_message(call.message.chat.id, answer:='Какую задачу вы хотите удалить?', reply_markup=keyboard)

    if call.data == "спросить ии":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, answer:='Что вы хотите спросить ии?'), ask_ai)

    if call.data in [' '.join(i) + ' - удалить' for i in get_all_tasks(call.message.chat.id)]:
        text = call.data.split()
        text = text[:-2]
        text = [' '.join(text[:-2]), ' '.join(text[-2:])]
        delete_task(call.message.chat.id, text[1], text[0])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Удалено!', reply_markup=keyboard_home)


    if call.data in [' '.join(i) + '' for i in get_all_tasks(call.message.chat.id)]:
        text = call.data.split()
        print(text)
        text = text
        text = [' '.join(text[:-2]), ' '.join(text[-2:])]
        print(text)
        mark_as_done(call.message.chat.id, text[1], text[0])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Выполнено!', reply_markup=keyboard_home)





@bot.message_handler(content_types=['voice'])   #поменяй как тебе надо
def voice_processing(message):
    recognizer = sr.Recognizer()
    filename = str(uuid.uuid4()) #рандомные названия(защита от неудаленных файлов)
    file_name_full= filename+ ".ogg"
    file_name_full_converted= filename+".wav"

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
         
    subprocess.call(['ffmpeg', '-i', file_name_full, file_name_full_converted])
    
    audio = sr.AudioFile(file_name_full_converted)
    #В try итоговый результат.
    try:                                     
        with audio as source:
            audio_data = recognizer.record(source) 
            text = recognizer.recognize_google(audio_data, language="ru-RU")
        bot.send_message(message.chat.id, text) #text это и есть то что прога услышала прога
    except: #в except добавь кнопку выхода или убери register_next_step_handler
        bot.reply_to(message, "Неразборчиво")
        
    #удаление временных файлов
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


def add_task_date(message):
    print(message)
    time_and_date = message.text
    print(time_and_date)
    f = open(f'newtask{message.chat.id}', 'a')
    f.write(f';{message.text}')
    f.close()
    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Описание?'), add_task_description)


def add_task_description(message):
    if message.content_type == 'voice':
        text = voice_processing1(message)
        f = open(f'newtask{message.chat.id}', 'a')
        f.write(f';{text}')
        f.close()
        bot.send_message(message.chat.id, 'записано', reply_markup=keyboard_home)
        f = open(f'newtask{message.chat.id}', 'r')
        a = f.readline().split(';')

        add_task(message.chat.id, a[0], a[1], a[2])
    else:
        f = open(f'newtask{message.chat.id}', 'a')
        f.write(f';{message.text}')
        f.close()
        bot.send_message(message.chat.id, 'записано', reply_markup=keyboard_home)
        f = open(f'newtask{message.chat.id}', 'r')
        a = f.readline().split(';')

        add_task(message.chat.id, a[0], a[1], a[2])



def get_keyboard(user_id, tag):
    keyboard_tasks = types.InlineKeyboardMarkup()
    buttons_tasks = [types.InlineKeyboardButton(f'{i[3]} {i[2]}', callback_data=f'{i[3]} {i[2]}') for i in get_tagged_tasks(user_id, tag)]
    keyboard_tasks.add(but_exit)
    for button in buttons_tasks:
        keyboard_tasks.add(button)
    return keyboard_tasks


def get_keyboard_for_del(user_id, tag):
    keyboard_tasks = types.InlineKeyboardMarkup()
    buttons_tasks = [types.InlineKeyboardButton(f'{i[3]} {i[2]} - удалить', callback_data=f'{i[3]} {i[2]} - удалить') for i in get_tagged_tasks(user_id, tag)]
    keyboard_tasks.add(but_exit)
    for button in buttons_tasks:
        keyboard_tasks.add(button)
    return keyboard_tasks


def get_keyboard_done(user_id, tag):
    keyboard_tasks = types.InlineKeyboardMarkup()
    buttons_tasks = [types.InlineKeyboardButton(f'{i[3]} {i[2]}', callback_data=f'{i[3]} {i[2]}') for i in get_tagged_tasks(user_id, tag)]
    keyboard_tasks.add(but_exit)
    for button in buttons_tasks:
        keyboard_tasks.add(button)
    return keyboard_tasks



def voice_processing1(message):
    recognizer = sr.Recognizer()
    filename = str(uuid.uuid4()) #рандомные названия(защита от неудаленных файлов)
    file_name_full= filename+ ".ogg"
    file_name_full_converted= filename+".wav"

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
         
    subprocess.call(['ffmpeg', '-i', file_name_full, file_name_full_converted])
    
    audio = sr.AudioFile(file_name_full_converted)
    #В try итоговый результат.
    try:                                     
        with audio as source:
            audio_data = recognizer.record(source) 
            text = recognizer.recognize_google(audio_data, language="ru-RU")
        os.remove(file_name_full)
        os.remove(file_name_full_converted)
        return text #text это и есть то что прога услышала прога
    except: #в except добавь кнопку выхода или убери register_next_step_handler
        bot.reply_to(message, "Неразборчиво")

def ask_ai(message):
    bot.send_message(message.chat.id, call_ai(message.text), reply_markup=keyboard_home)





bot.infinity_polling()