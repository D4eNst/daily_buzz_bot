import asyncio
import asyncpg
import logging

from .bot import dp, bot
from .telegram_bot.handlers import rg_msg_hd, rg_middlewares
from backend.database import utils
from yoomoney import Authorize, Client, Quickpay

logging.basicConfig(level=logging.INFO)


async def start_with():
    pool_connect: asyncpg.Pool = await utils.create_pool()
    async with pool_connect.acquire() as connect:
        db = utils.Database(connect)
        await db.create_tables()
    await pool_connect.close()

    logging.info("database has been connected")
    logging.warning("Bot has been started!")


async def stop_with():
    logging.warning("Bot has been stopped!")


async def start_bot():
    dp.startup.register(start_with)
    dp.shutdown.register(stop_with)

    pool_connect: asyncpg.Pool = await utils.create_pool()
    await rg_msg_hd(dp)
    await rg_middlewares(dp, pool_connect)
    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot)
    finally:
        await pool_connect.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
