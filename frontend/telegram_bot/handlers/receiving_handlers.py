from aiogram import types
from data import messages
from data.config import language, currency
from .keyboards import keyboards as kb
import backend.database.utils as db


async def subscribe(msg: types.Message) -> None:
    sub = True  # request to database
    status = " ✅ Активна"  # request to database
    finish = 14  # request to database

    status_text = f"{messages['subscribe']['status'][language]}<b>{status}</b>"
    finish_text = f" \n{messages['subscribe']['finish'][language]}<b>{finish}</b>"
    ans = f"{status_text}" if not sub else \
        f"{status_text}{finish_text}"
    await msg.answer(ans, reply_markup=kb.subscribe_kb())


async def variants(msg: types.Message) -> None:
    variants_list = ["1", "2", "3"]  # request to database

    variants_list_for_ans = "".join([f"\n <b> {variant} </b> " for variant in variants_list])
    ans = f"{ messages['variants'][language] }" + variants_list_for_ans

    await msg.answer(ans, reply_markup=kb.variants_kb())


async def balance(msg: types.Message) -> None:
    user = db.get_user(msg.from_user.id)
    bal = user.balance

    await msg.answer(f"{messages['balance'][language]}<b>{bal}</b> {currency}", reply_markup=kb.balance_kb())


async def info(msg: types.Message) -> None:
    status = " Bronze"  # request to database
    total_buy = 1234  # request to database
    total_sub = 4  # request to database

    login = msg.from_user.username

    ans = f"{messages['info']['login'][language]} <b>@{login}</b>" \
          f"\n{messages['info']['status'][language]} <b>{status}</b>" \
          f"\n{messages['info']['total_buy'][language]} <b>{total_buy}</b> {currency}" \
          f"\n{messages['info']['total_sub'][language]} <b>{total_sub}</b>"

    await msg.answer(ans, reply_markup=kb.info_kb())


async def history(msg: types.Message) -> None:
    stories = [{
        "date": "date of buy",
        "subscribe": "name of subscribe"
    }, {
        "date": "date of buy 2",
        "subscribe": "name of subscribe 2"
    }]  # request to database

    ans = "\n\n".join([f"{messages['history']['date'][language]}{story['date']}\n"
                       f"{messages['history']['name'][language]}{story['subscribe']}" for story in stories])

    await msg.answer(ans, reply_markup=kb.back_btn())
