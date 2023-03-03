from aiogram import types
from aiogram.dispatcher import FSMContext
from data import messages
from data.config import language, currency, min_replenishment_amount
from .keyboards import keyboards as kb
import frontend.telegram_bot.states as states
import backend.database.utils as db


async def add_balance(msg: types.Message):
    await msg.answer(f"{messages['add_balance'][language]}{min_replenishment_amount} {currency}",
                     reply_markup=kb.back_btn())
    await states.BalanceStatesGroup.WaitingPrice.set()


async def finish_balance(msg: types.Message, state: FSMContext):
    user = db.get_user(msg.from_user.id)
    try:
        quantity = int(msg.text)
        if True:
            user.replenish_balance(quantity)
            db.update_user(user)
        await state.finish()
        await msg.answer(f"{messages['add_balance']['replenished_suc'][language]}{user.balance} {currency}",
                         reply_markup=kb.main_menu_kb())
    except (ValueError, TypeError):
        await msg.reply(messages["errors"]["its_not_number"][language])
