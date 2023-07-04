import configparser
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from callbacks import *

config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

GROUP_ID = config.get('bot', 'group_id')
TOKEN = config.get('bot', 'token')

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
