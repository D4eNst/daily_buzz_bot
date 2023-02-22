from aiogram import Dispatcher, types
from aiogram.dispatcher import filters, FSMContext
from data.config import language, currency
from .keyboards import *
import yaml

with open('data/messages.yaml', encoding='utf-8') as stream:
    messages = yaml.load(stream, Loader=yaml.FullLoader)
with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)