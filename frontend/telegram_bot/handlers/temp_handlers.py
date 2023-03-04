from aiogram import types
from backend.database import utils as db


async def del_sub(msg: types.Message) -> None:
    user = db.get_user(msg.from_user.id)
    user.del_subscribe()
    db.update_user(user)
    await msg.answer("Подписка отменена")
