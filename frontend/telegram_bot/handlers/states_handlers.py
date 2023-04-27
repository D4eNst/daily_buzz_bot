from datetime import datetime
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from yoomoney import Client, Quickpay, History
# from aiogram.types import LabeledPrice, PreCheckoutQuery

from .keyboards import keyboards as kb, inline_keyboards as ikb
import frontend.telegram_bot.states as states
from backend.database.utils import Database
from backend.database.models import User, Product, History, get_final_price, get_status
from data.config import language, currency, min_replenishment_amount
from data import messages
from data import errors as e


async def add_balance(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(f"{messages['balance']['add_balance'][language]}{min_replenishment_amount} {currency}",
                     reply_markup=kb.back_btn())
    await state.set_state(states.BalanceStatesGroup.WAITING_PRICE)


async def confirm_pay(msg: types.Message, state: FSMContext) -> None:
    if msg.text.isdigit():
        quantity = int(msg.text)
        if quantity >= min_replenishment_amount:
            date_now = datetime.timestamp(datetime.now())
            label = f"{msg.from_user.id}-{int(date_now * 100)}-{quantity}"
            print(label)
            quickpay = Quickpay(
                receiver="4100117197160613",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=quantity,
                label=label
            )
            await state.set_state(states.BalanceStatesGroup.WAITING_PAY)
            await msg.answer(f'<a href="{quickpay.redirected_url}">{messages["pay"]["click_to_pay"][language]}</a>',
                             reply_markup=ikb.pay_btn(label))
        else:
            try:
                raise e.MinReplenishmentAmountError
            except e.MinReplenishmentAmountError as er:
                await msg.answer(f"{messages['balance']['replenished_err'][language]}{er.code}")
    else:
        await msg.reply(messages["errors"]["NaNError"][language])


async def finish_balance(callback: types.CallbackQuery, state: FSMContext, db: Database, client: Client, bot: Bot):
    await callback.answer()
    user = await db.get_user(callback.from_user.id)
    label = callback.data.split("_")
    label = label[1]
    quantity = int(label.split("-")[2])

    history: History = client.operation_history(label=label)
    if history.operations:
        # if True:
        operation = history.operations[0]
        if operation.status == "success":
            # if True:
            await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, None, None)
            user.replenish_balance(quantity)
            await db.update_user(user)
            await state.set_state(states.DefaultState.DEFAULT_STATE)
            await callback.message.answer(
                f"{messages['balance']['replenished_suc'][language]}{user.balance} {currency}",
                reply_markup=kb.main_menu_kb())
    else:
        await callback.message.answer(messages['pay']['waiting'][language])


async def buy_subscribe(msg: types.Message, state: FSMContext, db: Database) -> None:
    subs = await db.get_subscribes()
    if not subs:
        try:
            raise e.SubscriptionNotFoundError
        except e.SubscriptionNotFoundError as error:
            await msg.answer(f'{messages["errors"]["NoSubscriptionsAvailableError"][language]}\n'
                             f'error code: {error.code}', reply_markup=kb.personal_acc_kb())
            await state.clear()
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

        final_price = get_final_price(sub.price, user.status)
        await callback.message.answer(f"{messages['subscribe']['warning'][language]}{final_price} {currency}",
                                      reply_markup=kb.confirm_btn())

    except e.SubscriptionNotFoundError as er:
        await state.clear()
        await state.set_state(states.DefaultState.DEFAULT_STATE)
        await callback.answer("invalid button", show_alert=True)
        await callback.message.answer(f"{messages['errors']['SubscriptionNotFoundError'][language]}\n"
                                      f"Error code: {er.code}", reply_markup=kb.subscribe_kb())


async def confirm_subscribe(msg: types.Message, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    user = User(*data['user'])
    sub = Product(*data['sub'])
    try:
        final_price = get_final_price(sub.price, user.status)
        sub.price = final_price
        user.buy_subscribe(final_price, sub.period)
        user.status = get_status(user.total_buy)[0]
        purchase_history = History(tg_id=user.tg_id,
                                   product=sub,
                                   purchase_date=str(datetime.today()),
                                   current_status=user.status)
        await db.update_user(user)
        await db.add_history(purchase_history)
        await msg.answer(f'{messages["subscribe"]["confirm"][language]}')
    except e.InsufficientFundsError as error:
        await msg.answer(f'{messages["errors"]["InsufficientFundsError"][language]}\nError code: {error.code}')

    await msg.answer(messages["main_menu"][language], reply_markup=kb.main_menu_kb())
    await state.clear()
    await state.set_state(states.DefaultState.DEFAULT_STATE)
