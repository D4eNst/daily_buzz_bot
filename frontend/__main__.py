from aiogram import executor
from .bot import dp
from .telegram_bot.handlers import rg_msg_hd


async def on_startup(_) -> None:
    print("Bot has been started!")

if __name__ == "__main__":
    rg_msg_hd(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
