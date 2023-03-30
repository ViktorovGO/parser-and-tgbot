# импорт функции для поддержки работоспособности
# from background import keep_alive
from threading import Thread
from parser_1 import get_info
from random import randrange
import time
import json
from aiogram import Bot, Dispatcher, executor, types
import pip
import asyncio
pip.main(['install', 'aiogram'])
API_TOKEN = "5443440955:AAHSLQkvlMVbNOLXxXIAsiaaIqBn4lj8PG4"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_news(user_id):

    global article
    global new_state
    global prev_art_date
    new_state = False
    zakrep_published = False

    with open('artile_info.json', 'r') as f:
        article = json.load(f)
    if article[0]['zakrep'] != "":
        zakrep_published = True
        prev_zakrep_date = article[0]['date_pub']

    await bot.send_message(user_id, '_Новость от {}_'.format(article[0]['date_pub']), parse_mode='Markdown')
    await bot.send_photo(user_id, article[0]['img_art'])
    # await bot.send_message(user_id, 'Ссылка на новость:{}'.format(article[0]['original_url']))
    await bot.send_message(user_id, '*{}*'.format(article[0]['title']), parse_mode='Markdown')
    await bot.send_message(user_id, article[0]['text'])

    prev_art_date = article[0]['date_pub']

    while (1):
        get_info('https://dota2.ru/news/')
        await asyncio.sleep(randrange(30, 60))
        with open('artile_info.json', 'r') as f:
            article = json.load(f)
        if article[0]['zakrep'] != "" and article[0]['date_pub'] != prev_zakrep_date:

            zakrep_published == False
        if article[0]['date_pub'] != prev_art_date and article[0]['zakrep'] == "":

            new_state = True
        elif article[0]['zakrep'] != "" and article[0]['date_pub'] != prev_zakrep_date and zakrep_published == False:

            new_state = True
            prev_zakrep_date = article[0]['date_pub']
        elif zakrep_published == True and article[0]['zakrep'] != "" and article[0]['date_pub'] == prev_zakrep_date and article[1]['date_pub'] != prev_art_date:

            article[0], article[1] = article[1], article[0]
            new_state = True

        if new_state:
            await bot.send_message(user_id, '_Новость от {}_'.format(article[0]['date_pub']), parse_mode='Markdown')
            await bot.send_photo(user_id, article[0]['img_art'])
            # await bot.send_message(user_id, 'Ссылка на новость:{}'.format(article[0]['original_url']))
            await bot.send_message(user_id, '*{}*'.format(article[0]['title']), parse_mode='Markdown')
            await bot.send_message(user_id, article[0]['text'])
            prev_art_date = article[0]['date_pub']
            new_state = False


# Явно указываем в декораторе, на какую команду реагируем.
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    # Так как код работает асинхронно, то обязательно пишем await.
    await message.reply(f"Привет {user_full_name}!\nЯ новостной бот по дота 2, буду скидывать вам новости по мере их появления.")


# Явно указываем в декораторе, на какую команду реагируем.
@dp.message_handler(commands=['start_news'])
async def get_news(message: types.Message):
    get_info('https://dota2.ru/news/')
    global user_id
    user_id = message.from_user.id
    await bot.send_message(user_id, "Теперь вы будете получать новые новости по dota2 \U0001FAE1")
    loop = asyncio.get_event_loop()
    loop.create_task(send_news(user_id))

    # asyncio.run(if_new_state(new_state, prev_art_date))
    # Thread(target = if_new_state, args = (new_state, prev_art_date,)).start()


if __name__ == '__main__':
    # keep_alive()

    executor.start_polling(dp)
    # start_news_loop()
