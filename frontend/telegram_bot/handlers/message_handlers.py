import yaml
from aiogram import Dispatcher, types
from .keyboards import main_menu_kb


with open('data/messages.yaml', encoding='utf-8') as stream:
    messages = yaml.load(stream, Loader=yaml.FullLoader)


async def cmd_start(msg: types.Message) -> None:
    await msg.answer("It's command /start", reply_markup=main_menu_kb())


def rg_msg_hd(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
