from aiogram import Dispatcher, types


async def cmd_start(msg: types.Message) -> None:
    await msg.answer("Hi, it's my first start!")


def rg_msg_hd(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
