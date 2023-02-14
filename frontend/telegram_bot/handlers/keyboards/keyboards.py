import yaml
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import language

with open('data/buttons.yaml', encoding='utf-8') as stream:
    buttons = yaml.load(stream, Loader=yaml.FullLoader)


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


