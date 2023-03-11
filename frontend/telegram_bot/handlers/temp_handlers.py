from aiogram import types
from backend.database.utils import Database
from backend.database.models import User, Product, History


async def del_sub(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    user.del_product()
    await db.update_user(user)
    await msg.answer("Подписка отменена")


async def del_history(msg: types.Message, db: Database) -> None:
    pass


async def del_all_history(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    user.del_product()
    await db.update_user(user)
    await msg.answer("Подписка отменена")


async def add_subscribe(msg: types.Message, db: Database) -> None:
    txt = msg.text.split(" ")
    title = txt[1]
    period = int(txt[2])
    price = int(txt[3])
    sub = Product(product_type="Subscribe", title=title, period=period, price=price)
    await db.add_subscribe(sub)
    await msg.answer(f"Подписка {sub.title} добавлена")


async def del_product(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    sub_id = int(msg.text.split(' ')[1])
    product = await db.get_product(sub_id)
    await db.del_product(product)
    await msg.answer(f"Подписка {product.title} теперь неактивна")
