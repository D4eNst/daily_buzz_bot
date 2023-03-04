from aiogram import types
from aiogram.dispatcher import FSMContext

from data import messages
from data.config import language, currency, min_replenishment_amount
from .keyboards import keyboards as kb, inline_keyboards as ikb
import frontend.telegram_bot.states as states
from backend.database import utils as db
from backend.database.models import User, Subscribe
from data import errors as e


async def add_balance(msg: types.Message) -> None:
    await msg.answer(f"{messages['balance']['add_balance'][language]}{min_replenishment_amount} {currency}",
                     reply_markup=kb.back_btn())
    await states.BalanceStatesGroup.WaitingPrice.set()


async def finish_balance(msg: types.Message, state: FSMContext) -> None:
    user = db.get_user(msg.from_user.id)
    try:
        quantity = int(msg.text)
        if quantity >= min_replenishment_amount:
            user.replenish_balance(quantity)
            db.update_user(user)
            await state.finish()
            await msg.answer(f"{messages['balance']['replenished_suc'][language]}{user.balance} {currency}",
                             reply_markup=kb.main_menu_kb())
        else:
            error_kod = 1
            await state.finish()
            await msg.answer(f"{messages['balance']['replenished_err'][language]}{error_kod}",
                             reply_markup=kb.main_menu_kb())

    except (ValueError, TypeError):
        await msg.reply(messages["errors"]["NaNError"][language])


async def buy_subscribe(msg: types.Message) -> None:
    await msg.answer(messages["subscribe"]["choose"][language], reply_markup=ikb.list_subs())
    await msg.answer("Для отмены действия воспользуйтесь клавиатурой", reply_markup=kb.back_btn())
    await states.BuySubStatesGroup.choose.set()


async def choose_subscribe(callback: types.CallbackQuery, state: FSMContext) -> None:
    sub_id = int(callback.data[4:])
    sub = db.get_subscribe(sub_id)
    if not sub:
        await callback.answer(f"{messages['errors']['SubscriptionNotFoundError'][language]}\n"
                              f"Error code: {407}")  # TODO end
        await state.finish()
        return
    user = db.get_user(callback.from_user.id)
    async with state.proxy() as data:
        data["sub"] = sub.get_values(form=2)
        data["user"] = user.get_values(form=2)
    await callback.message.answer(f"{messages['subscribe']['warning'][language]}{sub.price} {currency}",
                                  reply_markup=kb.confirm_btn())
    await states.BuySubStatesGroup.next()


async def confirm_subscribe(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    user = User(*data['user'])
    sub = Subscribe(*data['sub'])
    try:
        user.buy_subscribe(sub.price, sub.period)
        db.update_user(user)
        await msg.answer(f'{messages["subscribe"]["confirm"][language]}')
    except e.InsufficientFundsError as error:
        await msg.answer(f'{messages["errors"]["InsufficientFundsError"][language]}\nError code: {error.code}')

    await msg.answer(messages["main_menu"][language], reply_markup=kb.main_menu_kb())
    await state.finish()

