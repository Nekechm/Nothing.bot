from aiogram import executor
from create_bot import dp
from bs4 import BeautifulSoup
import requests

async def on_startup(_):
    print('Бот в онлайне')

from handlers import client

client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)