from aiogram.types import InlineKeyboardMarkup
from data import buttons
from data.config import language
# from backend.database.utils import Database
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def list_subs(subs: list) -> InlineKeyboardMarkup:
    ikb_builder = InlineKeyboardBuilder()
    c = []
    for sub in subs:
        c.append(1)
        ikb_builder.button(
            text=sub.title,
            callback_data=f"sub:{sub.product_id}"
        )
    ikb_builder.adjust(*c)
    return ikb_builder.as_markup()


def arrows(right=True, left=True) -> InlineKeyboardMarkup:
    ikb_builder = InlineKeyboardBuilder()
    if left:
        ikb_builder.button(text="⬅", callback_data="arrow_back")
    if right:
        ikb_builder.button(text="➡", callback_data="arrow_next")
    return ikb_builder.as_markup()


def pay_btn(label) -> InlineKeyboardMarkup:
    ikb_builder = InlineKeyboardBuilder()
    ikb_builder.button(text=buttons['utils_buttons']['payed'][language], callback_data=f"pay_{label}")
    return ikb_builder.as_markup()
