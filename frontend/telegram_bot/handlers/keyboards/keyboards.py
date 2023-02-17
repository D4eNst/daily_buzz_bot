import yaml
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import language

with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)


def main_menu_btn() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard


def back_btn() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(utils_buttons["main_menu"][language]), KeyboardButton(utils_buttons["back"][language])]
    ], resize_keyboard=True)
    return keyboard


def main_menu_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    main_menu = buttons["main_menu"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(utils_buttons["personal_acc"][language])],
        [KeyboardButton(main_menu["about"][language]), KeyboardButton(main_menu["rules"][language])],
        [KeyboardButton(main_menu["help"][language])]
    ], resize_keyboard=True)
    return keyboard


def help_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    help_buttons = buttons["help"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(help_buttons["faq"][language]), KeyboardButton(utils_buttons["main_menu"][language])],
        [KeyboardButton(help_buttons["not_found_answer"][language])],
        [KeyboardButton(help_buttons["complaints"][language]), KeyboardButton(help_buttons["suggestions"][language])]
    ], resize_keyboard=True)
    return keyboard


def personal_acc_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    pers_acc_buttons = buttons["personal_acc"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(pers_acc_buttons["subscribe"][language]), KeyboardButton(pers_acc_buttons["info"][language])],
        [KeyboardButton(pers_acc_buttons["balance"][language]), KeyboardButton(pers_acc_buttons["history"][language])],
        [KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard


def subscribe_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    sub_buttons = buttons["subscribe"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(sub_buttons["buy_subscribe"][language]), KeyboardButton(sub_buttons["variants"][language])],
        [KeyboardButton(utils_buttons["back"][language]), KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard


def variants_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    variants_buttons = buttons["variants"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(variants_buttons["buy_subscribe"][language])],
        [KeyboardButton(utils_buttons["back"][language]), KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard


def balance_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    balance_buttons = buttons["balance"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(balance_buttons["deposit"][language]),
         KeyboardButton(balance_buttons["enter_coupon"][language])],
        [KeyboardButton(utils_buttons["back"][language]), KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard


def info_kb() -> ReplyKeyboardMarkup:
    utils_buttons = buttons["utils_buttons"]
    info_buttons = buttons["info"]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(info_buttons["upgrade_status"][language])],
        [KeyboardButton(utils_buttons["back"][language]), KeyboardButton(utils_buttons["main_menu"][language])]
    ], resize_keyboard=True)
    return keyboard
