from datetime import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext

from .keyboards import keyboards as kb, inline_keyboards as ikb
import frontend.telegram_bot.states as states
from backend.database.utils import Database
from backend.database.models import User, Product, History
from data.config import language, currency, min_replenishment_amount
from data import messages
from data import errors as e


async def add_balance(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(f"{messages['balance']['add_balance'][language]}{min_replenishment_amount} {currency}",
                     reply_markup=kb.back_btn())
    await state.set_state(states.BalanceStatesGroup.WAITING_PRICE)


async def finish_balance(msg: types.Message, state: FSMContext, db: Database) -> None:
    user = await db.get_user(msg.from_user.id)

    if msg.text.isdigit():
        quantity = int(msg.text)
        if quantity >= min_replenishment_amount:
            user.replenish_balance(quantity)
            await db.update_user(user)
            await state.set_state(states.DefaultState.DEFAULT_STATE)
            await msg.answer(f"{messages['balance']['replenished_suc'][language]}{user.balance} {currency}",
                             reply_markup=kb.main_menu_kb())
        else:
            try:
                raise e.MinReplenishmentAmountError
            except e.MinReplenishmentAmountError as er:
                await state.set_state(states.DefaultState.DEFAULT_STATE)
                await msg.answer(f"{messages['balance']['replenished_err'][language]}{er.code}",
                                 reply_markup=kb.main_menu_kb())
    else:
        await msg.reply(messages["errors"]["NaNError"][language])


async def buy_subscribe(msg: types.Message, state: FSMContext, db: Database) -> None:
    subs = await db.get_subscribes()
    if not subs:
        try:
            raise e.SubscriptionNotFoundError
        except e.SubscriptionNotFoundError as error:
            await msg.answer(f'{messages["errors"]["NoSubscriptionsAvailableError"][language]}\n'
                             f'error code: {error.code}', reply_markup=kb.personal_acc_kb())
            await state.set_state(states.DefaultState.DEFAULT_STATE)
            return
    await msg.answer(messages["subscribe"]["choose"][language], reply_markup=ikb.list_subs(subs))
    await msg.answer(messages["subscribe"]["choose"]["cansel"][language], reply_markup=kb.back_btn())
    await state.set_state(states.BuySubStatesGroup.CHOOSE)


async def choose_subscribe(callback: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    await callback.answer()
    sub_id = int(callback.data[4:])
    sub: Product = await db.get_product(sub_id)

    try:
        if not sub or sub.is_active == 0 or sub.product_type != "Subscribe":
            raise e.SubscriptionNotFoundError
        await state.set_state(states.BuySubStatesGroup.CONFIRM)

        user = await db.get_user(callback.from_user.id)
        data = await state.get_data()
        data["sub"] = sub.get_values(form=2)
        data["user"] = user.get_values(form=2)
        await state.set_data(data)

        await callback.message.answer(f"{messages['subscribe']['warning'][language]}{sub.price} {currency}",
                                      reply_markup=kb.confirm_btn())

    except e.SubscriptionNotFoundError as er:
        await state.set_state(states.DefaultState.DEFAULT_STATE)
        await callback.answer("invalid button", show_alert=True)
        await callback.message.answer(f"{messages['errors']['SubscriptionNotFoundError'][language]}\n"
                                      f"Error code: {er.code}", reply_markup=kb.subscribe_kb())


async def confirm_subscribe(msg: types.Message, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    user = User(*data['user'])
    sub = Product(*data['sub'])
    try:
        user.buy_subscribe(sub.price, sub.period)
        purchase_history = History(tg_id=user.tg_id, product=sub, purchase_date=str(datetime.today()))
        await db.update_user(user)
        await db.add_history(purchase_history)
        await msg.answer(f'{messages["subscribe"]["confirm"][language]}')
    except e.InsufficientFundsError as error:
        await msg.answer(f'{messages["errors"]["InsufficientFundsError"][language]}\nError code: {error.code}')

    await msg.answer(messages["main_menu"][language], reply_markup=kb.main_menu_kb())
    await state.set_state(states.DefaultState.DEFAULT_STATE)
