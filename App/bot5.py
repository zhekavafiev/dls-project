import logging
import os
import torch
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from aiogram.dispatcher import FSMContext
from main import handle
from PIL import Image

API_TOKEN = '5373418576:AAFyzloFVPxI_Ob2z8vTcdTsoKGZlu6Vy9Q'
class Form(StatesGroup):
    wait_content = State()
    wait_style_type = State()
    wait_style = State()
    wait_depth = State()
    wait_handle = State()


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = '''
Привет, <b>{}</b> меня зовут StyleTransferBot. Я занимаюсь преобразованием изобржений.
Для того, чтобы посмотреть что я имею необходимо будет дать мне 2 фото. Первое - 
фото которое хотелось бы обработать, а второе - тот стиль, в котором вы хотите его увидеть.
Если готовы попробовать мои умения, то поехали /origin_foto
    '''
    mes = text.format(message.from_user.first_name)
    await bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup = types.ReplyKeyboardRemove())

@dp.message_handler(commands=['origin_foto'])
async def seng_instruction(message):
    if not os.path.exists(f"./{message.chat.id}"):
        os.makedirs(f"./{message.chat.id}")
    await Form.wait_content.set()
    await message.reply('Жду фото для обработки')

@dp.message_handler(state=Form.wait_content, content_types=['photo'])
async def get_content(message: types.Message, state: FSMContext):
    time = datetime.now()
    file_name_content = f"./{message.chat.id}/content_{time}.jpg" #
    await message.photo[-1].download(file_name_content)
    async with state.proxy() as data:
        data['content'] = file_name_content
 
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    home = types.KeyboardButton(text="Загрузить стиль")
    custom = types.KeyboardButton(text="Использовать по умолчанию")
    keyboard.add(home, custom)
    await Form.next()
    await bot.send_message(message.chat.id, 'Какой стиль вы бы хотели попробовать?', reply_markup=keyboard)

@dp.message_handler(state=Form.wait_style_type)
async def get_style_type(message, state: FSMContext):
    if (message.text == 'Загрузить стиль'):
        async with state.proxy() as data:
           data['custom_style'] = True
        await Form.next()
        await bot.send_message(message.chat.id, 'Отлчино жду фото', reply_markup = types.ReplyKeyboardRemove())
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
        async with state.proxy() as data:
           data['custom_style'] = False
        await Form.next()
        await bot.send_message(message.chat.id, 'Во что рекомендовал бы попробовать', reply_markup = keyboard)
    else:
        await bot.send_message(message.chat.id, 'Моя твоя не понимать!)')

@dp.message_handler(state=Form.wait_style)
async def get_style(message, state: FSMContext):
    async with state.proxy() as data:
        custom_stile = data['custom_style']
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    min = types.KeyboardButton(text="Минимальная")
    mid = types.KeyboardButton(text="Средняя")
    max = types.KeyboardButton(text="Максимальная")
    keyboard.add(min, mid, max)
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
    async with state.proxy() as data:
        data['style'] = file_name_style
    await Form.next()
    await bot.send_message(message.chat.id, 'А теперь давай выберем глубино обработки', reply_markup = keyboard)

@dp.message_handler(state=Form.wait_depth)
async def select_deph(message, state: FSMContext):
    if (message.text == 'Минимальная'):
        depth = 30
    if (message.text == 'Средняя'):
        depth = 60
    if (message.text == 'Максимальная'):
        depth = 90
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    yes = types.KeyboardButton(text="Да!!!!")
    keyboard.add(yes)
    async with state.proxy() as data:
        data['depth'] = depth
    await Form.next()
    await bot.send_message(message.chat.id, 'Поехали?', reply_markup = keyboard)

@dp.message_handler(state=Form.wait_handle)
async def handlee(message, state: FSMContext):
    async with state.proxy() as data:
        path_to_file = os.path.abspath(data['content'])
        path_to_style = os.path.abspath(data['style'])
        chat_id = message.chat.id
        depth = data['depth']
    await state.finish()
    await handle(
        path_to_file,
        path_to_style,
        chat_id,
        depth
    )
    # for i in paths:
    #     await bot.send_photo(message.chat.id, photo = open(i, 'rb'))
    torch.cuda.empty_cache()
    await bot.send_message(message.chat.id, 'Если не понравилось, можем попробовать еще разок /origin_foto')

# @dp.message_handler(commands=['ph'])
# async def handlee(message):
#     await handle(
#         '173929967/content_2022-06-22 00:53:20.805026.jpg',
#         'default_stiles/mazki.jpg',
#         message.chat.id,
#         100
#     )
#     await bot.send_message(message.chat.id, 'Вроде все получилось, как тебе?')
#     await bot.send_message(message.chat.id, 'Если не понравилось, можем попробовать еще разок /origin_foto')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)