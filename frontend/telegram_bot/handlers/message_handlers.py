import yaml
from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from data.config import language
from .keyboards import main_menu_kb, help_kb


with open('data/messages.yaml', encoding='utf-8') as stream:
    messages = yaml.load(stream, Loader=yaml.FullLoader)
with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)


async def cmd_start(msg: types.Message) -> None:
    await msg.answer(messages["main_menu"][language], reply_markup=main_menu_kb())


async def main_menu(msg: types.Message) -> None:
    await msg.answer(messages["main_menu"][language], reply_markup=main_menu_kb())


async def cmd_help(msg: types.Message) -> None:
    await msg.answer(messages["help"][language], reply_markup=help_kb())


def rg_msg_hd(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(main_menu, filters.Text([buttons["utils_buttons"]["main_menu"][language]]))
    dp.register_message_handler(cmd_help, commands=['help'])
