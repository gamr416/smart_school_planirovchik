import speech_recognition as sr
import telebot
import os
import subprocess
import uuid
url = "8021686178:AAGmze85r7PUbYUw0jZRtqEEf3vGueP2NVI" #нахуй сноси
bot = telebot.TeleBot(url)





recognizer = sr.Recognizer()  



@bot.message_handler(content_types=['voice'])   #поменяй как тебе надо
def voice_processing(message):
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
        bot.register_next_step_handler(bot.send_message(message.chat.id, "повторите"),voice_processing)
    #удаление временных файлов
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


bot.infinity_polling()
