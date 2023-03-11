import datetime
from aiogram import types
from data import messages, errors as e
from data.config import language, currency
from .keyboards import keyboards as kb
from backend.database.utils import Database
from backend.database.models import User, History


async def subscribe(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    sub = user.subscribe
    sub_text = f"{messages['subscribe'][sub][language]}"
    finish = 0
    if sub:
        finish = user.subscribe_remains

    finish_text = f" \n{messages['subscribe']['finish'][language]}<b>{finish}</b>"
    status_text = f"{messages['subscribe']['status'][language]}<b>{sub_text}</b>"

    ans = f"{status_text}" if not sub else \
        f"{status_text}{finish_text}"
    await msg.answer(ans, reply_markup=kb.subscribe_kb())


async def variants(msg: types.Message, db: Database) -> None:
    subs = await db.get_subscribes()

    try:
        if not subs:
            raise e.SubscriptionNotFoundError
    except e.SubscriptionNotFoundError as error:
        await msg.answer(f'{messages["errors"]["NoSubscriptionsAvailableError"][language]}\n'
                         f'error code: {error.code}')
        return

    answer_list = []
    br = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    for sub in subs:
        answer_list.append(
            f"<b>{sub.title}</b>\n"
            f"{messages['subscribe']['period'][language]}<b>{sub.period}</b>\n"
            f"{sub.price} <b>{currency}</b>\n"
        )
    ans = f"{br}{br.join(answer_list)}{br}"
    await msg.answer(ans, reply_markup=kb.variants_kb())


async def balance(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
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


async def history(msg: types.Message, db: Database) -> None:
    user = User(msg.from_user.id)
    user_history = await db.get_history(user)
    answer_list = []
    count = 1
    for purchase in user_history:
        product_type = messages['product_type'][purchase['product'].product_type][language]
        purchase_date = datetime.datetime.strptime(purchase['history'].purchase_date, '%Y-%m-%d %H:%M:%S.%f')
        product_title = purchase['product'].title
        product_price = purchase['product'].price
        answer_list.append(
            f"{count}) {purchase_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"<b>{product_type}</b> {product_title}, <b>{product_price} {currency}</b>"
        )
        count += 1

    ans = 'Ваша история покупок:\n\n' + '\n------------------------------------\n'.join(answer_list)

    if ans != "":
        await msg.answer(ans, reply_markup=kb.personal_acc_kb())
    else:
        await msg.answer("История покупока отсутствует", reply_markup=kb.personal_acc_kb())
