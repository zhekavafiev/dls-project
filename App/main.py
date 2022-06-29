from handle import ImageHandler
from aiogram import Bot, Dispatcher, executor, types


async def handle(content, style, id, depth):
    API_TOKEN = '5373418576:AAFyzloFVPxI_Ob2z8vTcdTsoKGZlu6Vy9Q'

    bot = Bot(token=API_TOKEN)
    paths = ImageHandler(
        content,
        style,
        id,
        depth
    ).run()

    for i in paths:
        await bot.send_photo(id, photo = open(i, 'rb'))

    return 
