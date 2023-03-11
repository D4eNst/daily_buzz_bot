import aioredis
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from data.config import token

redis = aioredis.from_url("redis://localhost")
storage = RedisStorage(redis=redis)
bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(storage=storage)
