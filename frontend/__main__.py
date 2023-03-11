import asyncio
from .bot import dp, bot
from .telegram_bot.handlers import rg_msg_hd, rg_middlewares
from backend.database import utils


async def start_with():
    pool_connect = await utils.create_pool()
    async with pool_connect.acquire() as connect:
        db = utils.Database(connect)
        await db.create_tables()
    print("database has been connected")

    await rg_msg_hd(dp)
    await rg_middlewares(dp, pool_connect)
    print("Bot has been started!")


async def stop_with():
    print("Bye!")


async def start_bot():
    dp.startup.register(start_with)
    dp.shutdown.register(stop_with)
    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_bot())

