from aiogram import Dispatcher, Bot, types
from data.config import token

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
