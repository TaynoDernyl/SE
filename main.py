# Copyright 2025 SWAGNER
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import telebot
from telebot import types
import http
import requests
from pathlib import Path
import os

folder = Path("Books pdf")

api_key = "8572616475:AAGXsL5WRc-zCDUIawJAyQQWxddinvJ5EHE"

bot = telebot.TeleBot(api_key)

ban = []

admin_id = 7642314724

def search_ban_users(id):
    for i in range(len(ban)):
        if ban[i] == id:
            return True
    return False

def for_answer_admin(text):
    parts = text.split()
    
    if len(parts) < 3:
        return ""
    
    result = " ".join(parts[2:])
    return result

def search_in_files(name):
    print(f"Ищем книгу:{name}")
    name = name.lower()
    
    for file in folder.glob("*.pdf"):
        if file.stem == name:
            return file
    return False
def check_internet_requests():
    try:
        response = requests.get("http://www.google.com", timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

@bot.message_handler(commands=['start']) #При вводе /start
def start_function(message):
    if search_ban_users(message.chat.id) == False:
        bot.send_message(message.chat.id, "Вас приветствует бот по поиску книг SE, введите название книги:")
        if message.chat.id == 7761784061:
            bot.send_message(message.chat.id, "Ассалам алейкум шлюшка любимая") #Если пользователь любимая девушка
        elif message.chat.id == 7642314724:
            bot.send_message(message.chat.id, "Ассалам алейкум админ епта") #Если админ не с твинка зашел

@bot.message_handler(commands=['help']) #При вводе /help
def help_function(message):
    if search_ban_users(message.chat.id) == False:
        bot.send_message(message.chat.id, "Для поиска и скачивания, напишите название книги в чат с ботом\n"
        "Кодер:@SWAGNERRR\n"
        "Создатель:@quethraa\n"
        "Для обращения в поддержку напишите:\n/support \"ваше сообщение в поддержку\"")

@bot.message_handler(commands=['support']) #При вводе /support
def support_function(message):
    if search_ban_users(message.chat.id) == False:
        try:
            bot.send_message(7642314724, f"{message.text}, id:{message.chat.id}")
            bot.send_message(message.chat.id, "Ваше сообщение доставлено админу на модерацию")
        except:
            bot.send_message(message.chat.id, "Проблема с ботом, повторите запрос позже")

@bot.message_handler(commands=['answer']) #--Для админа
def answer_function(message):
    if message.chat.id == 7642314724:
        text = for_answer_admin(message.text)
        temp = message.text.split()
        id = temp[1]
        bot.send_message(int(id), "Вы недавно обращались в поддержку, вам поступил ответ:\n"+text)

@bot.message_handler(commands=['ban'])
def ban_function(message):
    if message.chat.id == 7642314724:
        text = message.text.split()
        if len(text) > 1:
            if text[1] != str(admin_id):
                try:
                    if int(text[1]) not in ban:
                        ban.append(int(text[1]))
                        if len(text) > 2:
                            reason = " ".join(text[2:])
                            bot.send_message(int(text[1]), f"Бан по причине:{reason}")
                        bot.send_message(admin_id, f"Забанен пользователь с айди: {text[1]}")
                except:
                    bot.send_message(admin_id, "Ошибка")
            else:
                bot.send_message(message.chat.id, "Админа забанить нельзя xD")

@bot.message_handler(commands=['unban'])
def ban_function(message):
    if message.chat.id == 7642314724:
        text = message.text.split()
        try:
            ban.remove(int(text[1]))
            bot.send_message(admin_id, f"Разбанен пользователь с айди: {int(text[1])}")
        except:
            bot.send_message(message.chat.id, "Ошибка разбана")

@bot.message_handler(content_types=['text'])
def search_book(message): 
    if search_ban_users(message.chat.id) == False:
        if check_internet_requests(): #Если с инетом все норм
            print(f"возможный поиск книги:{message.text}, айди: {message.chat.id}")
            bot.send_message(message.chat.id, f"Ищем книгу с названием: {message.text}...")
            path = search_in_files(message.text)
            if path == False:
                bot.send_message(message.chat.id, "К сожалению в наших источниках такой книги не найдено")
            else:
                print(path)
                with open(path, "rb") as f:
                    bot.send_document(message.chat.id, f) 
        else:
            print("Ошибка сервера, попробуйте позже")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)