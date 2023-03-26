from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database

TOKEN = '5891234886:AAEsKfnbERu3-KCm0NjGbnYmPWb7g3rnwRo'
BOT_NAME = 'Nothinga_bot'
KASSA_TOKEN = '381764678:TEST:53276'
db = Database('Database1.db')


storage=MemoryStorage()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

