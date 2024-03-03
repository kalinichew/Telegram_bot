import telebot
from telebot import types # для указание типов
from dotenv import load_dotenv
import os
import requests
import json
from translate import Translator



load_dotenv(dotenv_path="tokens.env")
bot_token = os.getenv("BOT_TOKEN1")
if bot_token is None:
    raise ValueError("Токен не найден")



bot = telebot.TeleBot(bot_token)

def translate_text(text, target_language='ru'):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пришли ответ: Да или Нет")
    btn2 = types.KeyboardButton("Хочу фото пёселя")
    btn3 = types.KeyboardButton("Хочу анекдот про Чака Норриса")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, text="Это фановый бот. Выбери, что тебе нужно", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Пришли ответ: Да или Нет"):
        url ='https://yesno.wtf/api'
        response = requests.get(url)
        response_json = response.json()
        image = response_json['image']
        bot.send_video(message.chat.id, image, None, 'Text')
    elif(message.text == "Хочу фото пёселя"):
         url ='https://random.dog/woof.json'
         response = requests.get(url)
         response_json = response.json()
         image = response_json['url']
         bot.send_photo(message.chat.id, image, None, 'Text')
    elif(message.text == "Хочу анекдот про Чака Норриса"):
         url ='https://geek-jokes.sameerkumar.website/api?format=json'
         response = requests.get(url)
         response_json = response.json()
         messageJoke = response_json['joke']
         jokerus = translate_text(messageJoke, target_language='ru')
         bot.send_message(message.from_user.id, jokerus)
    else:
        bot.send_message(message.from_user.id, "Чтобы начать напиши /start")
        

bot.polling(none_stop=True)


