import frontend.telegram_bot.states as states
from frontend.telegram_bot.states import ds
from aiogram import filters, Dispatcher, F

from data.config import language
from data import buttons
from frontend.telegram_bot.middlewares import DbSession, CheckStates, VerifyUser, CountUpdates
from frontend.bot import redis

from .receiving_handlers import subscribe, variants, info, balance, history, change_history
from .states_handlers import add_balance, confirm_pay, finish_balance, buy_subscribe, choose_subscribe, confirm_subscribe
from .basic_handlers import cmd_start, cmd_help, faq, rules, about, \
    upgrade_status, main_menu, personal_acc, default_handler

from .temp_handlers import *  # TODO delete test file


async def rg_msg_hd(dp: Dispatcher) -> None:
    dp.message.register(cmd_start, filters.Command(commands=['start']))
    dp.message.register(cmd_help, F.text == buttons["main_menu"]["help"][language], ds)
    dp.message.register(faq, F.text == buttons["help"]["faq"][language], ds)
    dp.message.register(upgrade_status, F.text == buttons["info"]["upgrade_status"][language], ds)

    dp.message.register(rules, F.text == buttons["main_menu"]["rules"][language], ds)
    dp.message.register(about, F.text == buttons["main_menu"]["about"][language], ds)
    dp.message.register(main_menu, F.text == buttons["utils_buttons"]["main_menu"][language])
    dp.message.register(personal_acc,
                        (F.text == buttons["utils_buttons"]["personal_acc"][language]) |
                        (F.text == buttons["utils_buttons"]["back"][language]))

    dp.message.register(subscribe, F.text == buttons["personal_acc"]["subscribe"][language], ds)
    dp.message.register(balance, F.text == buttons["personal_acc"]["balance"][language], ds)
    dp.message.register(info, F.text == buttons["personal_acc"]["info"][language], ds)
    dp.message.register(history, F.text == buttons["personal_acc"]["history"][language], ds)
    dp.callback_query.register(change_history, filters.Text(startswith="arrow"), states.HistoryState.HISTORY)

    dp.message.register(add_balance, F.text == buttons["balance"]["deposit"][language], ds)
    dp.message.register(confirm_pay, states.BalanceStatesGroup.WAITING_PRICE)

    dp.message.register(buy_subscribe, F.text == buttons["subscribe"]["buy_subscribe"][language], ds)
    dp.message.register(variants, F.text == buttons["subscribe"]["variants"][language], ds)

    dp.callback_query.register(finish_balance)

    dp.callback_query.register(choose_subscribe, filters.Text(startswith="sub_"), states.BuySubStatesGroup.CHOOSE)
    dp.message.register(confirm_subscribe, filters.Text(buttons["utils_buttons"]["confirm"][language]),
                        states.BuySubStatesGroup.CONFIRM)

    dp.message.register(del_sub, filters.Command(commands=['del_sub']))
    dp.message.register(add_subscribe, filters.Command(commands=['add_subscribe']))
    dp.message.register(del_product, filters.Command(commands=['del_product']))



    dp.message.register(default_handler)


async def rg_middlewares(dp: Dispatcher, pool_connect) -> None:
    dp.update.middleware.register(CountUpdates())
    dp.message.middleware.register(VerifyUser(redis))
    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(CheckStates())
