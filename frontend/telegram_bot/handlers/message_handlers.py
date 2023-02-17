from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from data.config import language, currency
from .keyboards import *
import yaml

with open('data/messages.yaml', encoding='utf-8') as stream:
    messages = yaml.load(stream, Loader=yaml.FullLoader)
with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)


async def cmd_start(msg: types.Message) -> None:
    await msg.answer(messages["main_menu"][language], reply_markup=main_menu_kb())


async def main_menu(msg: types.Message) -> None:
    await msg.answer(messages["main_menu"][language], reply_markup=main_menu_kb())


async def cmd_help(msg: types.Message) -> None:
    await msg.answer(messages["help"][language], reply_markup=help_kb())


async def faq(msg: types.Message) -> None:
    await msg.answer(messages["faq"][language], reply_markup=main_menu_btn())


async def rules(msg: types.Message) -> None:
    await msg.answer(messages["rules"][language], reply_markup=main_menu_btn())


async def about(msg: types.Message) -> None:
    await msg.answer(messages["about"][language], reply_markup=main_menu_btn())


async def personal_acc(msg: types.Message) -> None:
    await msg.answer(messages["personal_acc"][language], reply_markup=personal_acc_kb())


async def subscribe(msg: types.Message) -> None:
    sub = True  # request to database
    status = " ✅ Активна"  # request to database
    finish = 14  # request to database

    status_text = f"{messages['subscribe']['status'][language]}<b>{status}</b>"
    finish_text = f" \n{messages['subscribe']['finish'][language]}<b>{finish}</b>"
    ans = f"{status_text}" if not sub else \
        f"{status_text}{finish_text}"
    await msg.answer(ans, reply_markup=subscribe_kb())


async def variants(msg: types.Message) -> None:
    variants_list = ["1", "2", "3"]  # request to database

    variants_list_for_ans = "".join([f"\n <b> {variant} </b> " for variant in variants_list])
    ans = f"{ messages['variants'][language] }" + variants_list_for_ans

    await msg.answer(ans, reply_markup=variants_kb())


async def balance(msg: types.Message) -> None:
    bal = 123  # request to database

    await msg.answer(f"{messages['balance'][language]}<b>{bal}</b>", reply_markup=balance_kb())


async def info(msg: types.Message) -> None:
    status = " Bronze"  # request to database
    total_buy = 1234  # request to database
    total_sub = 4  # request to database

    login = msg.from_user.username

    ans = f"{messages['info']['login'][language]} <b>@{login}</b>" \
          f"\n{messages['info']['status'][language]} <b>{status}</b>" \
          f"\n{messages['info']['total_buy'][language]} <b>{total_buy}</b> {currency}" \
          f"\n{messages['info']['total_sub'][language]} <b>{total_sub}</b>"

    await msg.answer(ans, reply_markup=info_kb())


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

    await msg.answer(ans, reply_markup=back_btn())


async def upgrade_status(msg: types.Message) -> None:
    await msg.answer(messages["upgrade_status"][language], reply_markup=back_btn())


def rg_msg_hd(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, filters.Text([buttons["main_menu"]["help"][language], "/help"]))

    dp.register_message_handler(main_menu, filters.Text(buttons["utils_buttons"]["main_menu"][language]))
    dp.register_message_handler(personal_acc, filters.Text([buttons["utils_buttons"]["personal_acc"][language],
                                                            buttons["utils_buttons"]["back"][language]]))

    dp.register_message_handler(rules, filters.Text(buttons["main_menu"]["rules"][language]))
    dp.register_message_handler(about, filters.Text(buttons["main_menu"]["about"][language]))

    dp.register_message_handler(subscribe, filters.Text(buttons["personal_acc"]["subscribe"][language]))
    dp.register_message_handler(balance, filters.Text(buttons["personal_acc"]["balance"][language]))
    dp.register_message_handler(info, filters.Text(buttons["personal_acc"]["info"][language]))
    dp.register_message_handler(history, filters.Text(buttons["personal_acc"]["history"][language]))

    dp.register_message_handler(upgrade_status, filters.Text(buttons["info"]["upgrade_status"][language]))
    dp.register_message_handler(variants, filters.Text(buttons["subscribe"]["variants"][language]))
    dp.register_message_handler(faq, filters.Text(buttons["help"]["faq"][language]))
