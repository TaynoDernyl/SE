import telebot
from telebot import types
import http
import requests

api_key = "8572616475:AAGXsL5WRc-zCDUIawJAyQQWxddinvJ5EHE"

bot = telebot.TeleBot(api_key)



def search_in_internet(name):
    print(f"Ищем в интернете книгу:{name}")

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
    bot.send_message(message.chat.id, "Вас приветствует бот по поиску книг SE, введите название книги:")
    if message.chat.id == 7761784061:
        bot.send_message(message.chat.id, "Ассалам алейкум шлюшка любимая") #Если пользователь любимая девушка
    elif message.chat.id == 7642314724:
        bot.send_message(message.chat.id, "Ассалам алейкум админ епта") #Если админ не с твинка зашел

@bot.message_handler(content_types=['text'])
def search_book(message): 
    if check_internet_requests(): #Если с инетом все норм
        print(f"возможный поиск книги:{message.text}, айди: {message.chat.id}")
        bot.send_message(message.chat.id, f"Ищем книгу с названием: {message.text}...")
        search_in_internet(message.text)
    else:
        print("Ошибка сервера, попробуйте позже")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)