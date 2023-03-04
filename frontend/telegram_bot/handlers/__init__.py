from aiogram.dispatcher import filters, Dispatcher
from data.config import language
from data import buttons
import frontend.telegram_bot.states as states

from .basic_handlers import cmd_start, cmd_help, faq, rules, about, upgrade_status, main_menu, personal_acc
from .receiving_handlers import subscribe, variants, info, balance, history
from .states_handlers import add_balance, finish_balance, buy_subscribe, choose_subscribe, confirm_subscribe

from .temp_handlers import *  # TODO delete test file


def rg_msg_hd(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, filters.Text([buttons["main_menu"]["help"][language], "/help"]))

    dp.register_message_handler(main_menu, filters.Text(buttons["utils_buttons"]["main_menu"][language]), state='*')
    dp.register_message_handler(personal_acc, filters.Text([buttons["utils_buttons"]["personal_acc"][language],
                                                            buttons["utils_buttons"]["back"][language]]), state="*")

    dp.register_message_handler(rules, filters.Text(buttons["main_menu"]["rules"][language]))
    dp.register_message_handler(about, filters.Text(buttons["main_menu"]["about"][language]))

    dp.register_message_handler(subscribe, filters.Text(buttons["personal_acc"]["subscribe"][language]))
    dp.register_message_handler(balance, filters.Text(buttons["personal_acc"]["balance"][language]))
    dp.register_message_handler(info, filters.Text(buttons["personal_acc"]["info"][language]))
    dp.register_message_handler(history, filters.Text(buttons["personal_acc"]["history"][language]))

    dp.register_message_handler(add_balance, filters.Text(buttons["balance"]["deposit"][language]))

    dp.register_message_handler(buy_subscribe, filters.Text(buttons["subscribe"]["buy_subscribe"][language]))

    dp.register_message_handler(upgrade_status, filters.Text(buttons["info"]["upgrade_status"][language]))
    dp.register_message_handler(variants, filters.Text(buttons["subscribe"]["variants"][language]))
    dp.register_message_handler(faq, filters.Text(buttons["help"]["faq"][language]))

    dp.register_message_handler(finish_balance, state=states.BalanceStatesGroup.WaitingPrice)

    dp.register_callback_query_handler(choose_subscribe, filters.Text(startswith="sub_"),
                                       state=states.BuySubStatesGroup.choose)
    dp.register_message_handler(confirm_subscribe, filters.Text(buttons["utils_buttons"]["confirm"][language]),
                                state=states.BuySubStatesGroup.confirm)

    dp.register_message_handler(del_sub, commands=["del_sub"])  # TODO delete test handlers
