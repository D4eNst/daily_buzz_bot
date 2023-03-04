from aiogram import types
from aiogram.dispatcher import FSMContext
from data import messages
from data.config import language
from backend.database import models, utils as db
from .keyboards import keyboards as kb


async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await state.finish()
    user = models.User(msg.from_user.id)
    if not db.get_user(user.tg_id):
        db.add_user(user)

    await msg.answer(messages["main_menu"][language], reply_markup=kb.main_menu_kb())


async def main_menu(msg: types.Message, state: FSMContext) -> None:
    await state.finish()
    await msg.answer(messages["main_menu"][language], reply_markup=kb.main_menu_kb())


async def cmd_help(msg: types.Message) -> None:
    await msg.answer(messages["help"][language], reply_markup=kb.help_kb())


async def faq(msg: types.Message) -> None:
    await msg.answer(messages["faq"][language], reply_markup=kb.main_menu_btn())


async def rules(msg: types.Message) -> None:
    await msg.answer(messages["rules"][language], reply_markup=kb.main_menu_btn())


async def about(msg: types.Message) -> None:
    await msg.answer(messages["about"][language], reply_markup=kb.main_menu_btn())


async def personal_acc(msg: types.Message, state: FSMContext) -> None:
    await state.finish()
    await msg.answer(messages["personal_acc"][language], reply_markup=kb.personal_acc_kb())


async def upgrade_status(msg: types.Message) -> None:
    await msg.answer(messages["upgrade_status"][language], reply_markup=kb.back_btn())
