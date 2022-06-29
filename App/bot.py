import telebot
from telebot import types

from datetime import datetime
import os

import torch
from main import handle
from PIL import Image

bot = telebot.TeleBot('5373418576:AAFyzloFVPxI_Ob2z8vTcdTsoKGZlu6Vy9Q')
    
@bot.message_handler(commands=['start'])
def start(message):
    text = '''
Привет, <b>{}</b> меня зовут StyleTransferBot. Я занимаюсь преобразованием изобржений.
Для того, чтобы посмотреть что я имею необходимо будет дать мне 2 фото. Первое - 
фото которое хотелось бы обработать, а второе - тот стиль, в котором вы хотите его увидеть.
Если готовы попробовать мои умения, то поехали /origin_foto
    '''
    mes = text.format(message.from_user.first_name)
    bot.send_message(message.chat.id, mes, parse_mode='html')

@bot.message_handler(commands=['origin_foto'])
def seng_instruction(message):
    if not os.path.exists(f"./{message.chat.id}"):
        os.makedirs(f"./{message.chat.id}")
    bot.send_message(message.chat.id, 'Жду фото для обработки')
    bot.register_next_step_handler(message, get_origin)
 
def get_origin(message):
    time = datetime.now()
    file_path_content = bot.get_file(message.photo[-1].file_id).file_path
    file_content = bot.download_file(file_path_content)
    file_name_content = f"./{message.chat.id}/content_{time}.jpg"
    with open(file_name_content, "wb") as code:
        code.write(file_content)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    home = types.KeyboardButton(text="Загрузить стиль")
    custom = types.KeyboardButton(text="Использовать по умолчанию")
    keyboard.add(home, custom)
    bot.send_message(message.chat.id, 'Какой стиль вы бы хотели попробовать?', reply_markup=keyboard)

    bot.register_next_step_handler(message, get_answer, file_name_content)

def get_answer(message, file_name_content):
    if (message.text == 'Загрузить стиль'):
        bot.send_message(message.chat.id, 'Отлчино жду фото', reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_style, file_name_content, True)
    elif (message.text == 'Использовать по умолчанию'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        van_gog = types.KeyboardButton(text="Ван гог")
        pikasso = types.KeyboardButton(text="Пикассо")
        cosmos = types.KeyboardButton(text="Космос")
        biutiful_lists = types.KeyboardButton(text="Мазки")
        green_lines = types.KeyboardButton(text="Зеленые линии")
        lava = types.KeyboardButton(text="Лава")
        led = types.KeyboardButton(text="Лёд")
        keyboard.add(van_gog, pikasso, cosmos, biutiful_lists, green_lines, lava, led)
        bot.send_message(message.chat.id, 'Во что рекомендовал бы попробовать', reply_markup = keyboard)
        bot.register_next_step_handler(message, get_style, file_name_content, False)
    else:
        bot.send_message(message.chat.id, 'Моя твоя не понимать!)')

def get_style(message, file_name_content, custom_stile):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    min = types.KeyboardButton(text="Минимальная")
    mid = types.KeyboardButton(text="Средняя")
    max = types.KeyboardButton(text="Максимальная")
    keyboard.add(min, mid, max)
    bot.send_message(message.chat.id, 'А теперь давай выберем глубино обработки', reply_markup = keyboard)
    if (custom_stile):
        time = datetime.now()
        file_path_style = bot.get_file(message.photo[-1].file_id).file_path
        file_style = bot.download_file(file_path_style)
        file_name_style = f"./{message.chat.id}/style_{time}.jpg"
        with open(file_name_style, "wb") as code:
            code.write(file_style)
    else:
        if (message.text == 'Ван гог'):
            file_name_style = "./default_stiles/van_gog.jpg"
        if (message.text == 'Пикассо'):
            file_name_style = "./default_stiles/pikasso.jpeg"
        if (message.text == 'Космос'):
            file_name_style = "./default_stiles/kosmos.jpg"
        if (message.text == 'Мазки'):
            file_name_style = "./default_stiles/mazki.jpg"
        if (message.text == 'Лава'):
            file_name_style = "./default_stiles/lava.jpg"
        if (message.text == 'Лёд'):
            file_name_style = "./default_stiles/led.jpg"
    bot.register_next_step_handler(message, select_deph, file_name_content, file_name_style)

def select_deph(message, file_name_content, file_name_style):
    if (message.text == 'Минимальная'):
        depth = 30
    if (message.text == 'Средняя'):
        depth = 60
    if (message.text == 'Максимальная'):
        depth = 90
    bot.send_message(message.chat.id, 'Ну поехали) Как все сделаю дам ответ', reply_markup = types.ReplyKeyboardRemove())
#     bot.register_next_step_handler(message, photo_send, file_name_content, file_name_style, depth)

# async def photo_send(message, file_name_content, file_name_style, depth):
    # bot.send_message(message.chat.id, 'Вроде все получилось, как тебе?')

    paths = handle(os.path.abspath(file_name_content), os.path.abspath(file_name_style), message.chat.id, depth)
    bot.send_message(message.chat.id, 'Вроде все получилось, как тебе?')

    for i in paths:
        image = Image.open(i)
        bot.send_photo(message.chat.id, image)
    torch.cuda.empty_cache()
    bot.send_message(message.chat.id, 'Если не понравилось, можем попробовать еще разок /origin_foto')

bot.polling(non_stop=True)
