from datetime import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from data import messages, errors as e
from data.config import language, currency
from .keyboards import keyboards as kb, inline_keyboards as ikb
from backend.database.utils import Database
from backend.database.models import User, get_final_price, get_status
from frontend.telegram_bot import states


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
    user = await db.get_user(msg.from_user.id)

    try:
        if not subs:
            raise e.SubscriptionNotFoundError
    except e.SubscriptionNotFoundError as error:
        await msg.answer(f'{messages["errors"]["NoSubscriptionsAvailableError"][language]}\n'
                         f'error code: {error.code}')
        return

    answer_list = []
    br = "➖➖➖➖➖➖➖➖➖➖➖\n"
    for sub in subs:
        answer_list.append(
            f"<b>{sub.title}</b>\n"
            f"{messages['subscribe']['period'][language]}<b>{sub.period}</b>\n"
            f"{sub.price} <b>{currency}</b>\n"
        )

        final_price = get_final_price(sub.price, user.status)
        if final_price != sub.price:
            answer_list[-1] = answer_list[-1].replace(f"{sub.price} <b>{currency}</b>",
                                                      f"<s>{sub.price} <b>{currency}</b></s>   "
                                                      f"{final_price} <b>{currency}</b>")
    ans = f"{br}{br.join(answer_list)}{br}"
    await msg.answer(ans, reply_markup=kb.variants_kb())


async def balance(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    bal = user.balance

    await msg.answer(f"{messages['balance'][language]}<b>{bal}</b> {currency}", reply_markup=kb.balance_kb())


async def info(msg: types.Message, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)
    total_buy = user.total_buy
    status = get_status(total_buy)[1]
    login = msg.from_user.username

    ans = f"{messages['info']['login'][language]} <b>@{login}</b>" \
          f"\n{messages['info']['status'][language]} <b>{status}</b>" \
          f"\n{messages['info']['total_buy'][language]} <b>{total_buy}</b> {currency}"

    await msg.answer(ans, reply_markup=kb.info_kb())


async def history(msg: types.Message, state: FSMContext, db: Database) -> None:
    user = User(msg.from_user.id)
    user_history = await db.get_history(user)
    answer_list = []
    pages = []

    def create_page(ans_list, page_num, step=5):
        page_start = (page_num - 1) * 5
        page_end = page_start + step
        return '\n------------------------------------\n'.join(ans_list[page_start:page_end])

    for count, purchase in enumerate(user_history, 1):
        product_type = messages['product_type'][purchase['product'].product_type][language]
        purchase_date = datetime.strptime(purchase['history'].purchase_date, '%Y-%m-%d %H:%M:%S.%f')
        product_title = purchase['product'].title
        product_price = get_final_price(purchase['product'].price, purchase['history'].current_status)
        answer_list.append(
            f"{count}) {purchase_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"<b>{product_type}</b> {product_title}, <b>{product_price} {currency}</b>"
        )
        if count % 5 == 0:
            pages.append(create_page(answer_list, count // 5))
    if (len(answer_list)) % 5 != 0:
        pages.append(create_page(answer_list, (len(answer_list) // 5) + 1, len(answer_list) % 5))

    await msg.answer('Ваша история покупок:\n\n', reply_markup=kb.back_btn())

    if answer_list:
        page = 1
        ans = pages[page - 1]
        if len(pages) > 1:
            await msg.answer(ans, reply_markup=ikb.arrows(left=False))
            await state.set_state(states.HistoryState.HISTORY)
            await state.set_data({
                'pages': pages,
                'page': page
            })
        else:
            await msg.answer(ans, reply_markup=kb.back_btn())
    else:
        await msg.answer("История покупока отсутствует", reply_markup=kb.personal_acc_kb())


async def change_history(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pages = data['pages']
    if callback.data == 'arrow_next':
        page = data['page'] + 1
    else:
        page = data['page'] - 1
    left = False if page == 1 else True
    right = False if page == (len(pages)) else True

    data['page'] = page
    await state.update_data(data)
    try:
        new_text = pages[page - 1]
        await callback.message.edit_text(new_text, callback.inline_message_id, reply_markup=ikb.arrows(right, left))
    except (IndexError, TelegramBadRequest):
        await callback.answer('Error')
