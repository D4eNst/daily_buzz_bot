from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data import buttons
from data.config import language


def remove_kb():
    return ReplyKeyboardRemove


def main_menu_btn() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def back_btn() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            ),
            KeyboardButton(
                text=utils_buttons["back"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def confirm_btn() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=utils_buttons["confirm"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            ),
            KeyboardButton(
                text=utils_buttons["back"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def main_menu_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    main_menu = buttons["main_menu"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=utils_buttons["personal_acc"][language]
            )
        ],
        [
            KeyboardButton(
                text=main_menu["about"][language]
            ),
            KeyboardButton(
                text=main_menu["rules"][language]
            )
        ],
        [
            KeyboardButton(
                text=main_menu["help"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def help_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    help_buttons = buttons["help"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=help_buttons["faq"][language]
            ),
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ],
        [
            KeyboardButton(
                text=help_buttons["not_found_answer"][language]
            )
        ],
        [
            KeyboardButton(
                text=help_buttons["complaints"][language]
            ),
            KeyboardButton(
                text=help_buttons["suggestions"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def personal_acc_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    pers_acc_buttons = buttons["personal_acc"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=pers_acc_buttons["subscribe"][language]
            ),
            KeyboardButton(
                text=pers_acc_buttons["info"][language]
            )
        ],
        [
            KeyboardButton(
                text=pers_acc_buttons["balance"][language]
            ),
            KeyboardButton(
                text=pers_acc_buttons["history"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def subscribe_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    sub_buttons = buttons["subscribe"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=sub_buttons["buy_subscribe"][language]
            ),
            KeyboardButton(
                text=sub_buttons["variants"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["back"][language]
            ),
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def variants_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    variants_buttons = buttons["variants"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=variants_buttons["buy_subscribe"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["back"][language]
            ),
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def balance_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    balance_buttons = buttons["balance"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=balance_buttons["deposit"][language]
            ),
            KeyboardButton(
                text=balance_buttons["enter_coupon"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["back"][language]
            ),
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard


def info_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    info_buttons = buttons["info"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(
                text=info_buttons["upgrade_status"][language]
            )
        ],
        [
            KeyboardButton(
                text=utils_buttons["back"][language]
            ),
            KeyboardButton(
                text=utils_buttons["main_menu"][language]
            )
        ]
    ], resize_keyboard=True)
    return keyboard
