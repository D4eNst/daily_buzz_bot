from aiogram.types import InlineKeyboardMarkup
# from data import buttons
# from data.config import language
# from backend.database.utils import Database
from aiogram.utils.keyboard import InlineKeyboardBuilder


def list_subs(subs: list) -> InlineKeyboardMarkup:
    ikb_builder = InlineKeyboardBuilder()
    c = []
    for sub in subs:
        c.append(1)
        ikb_builder.button(
            text=sub.title,
            callback_data=f"sub_{sub.product_id}"
        )
    ikb_builder.adjust(*c)
    return ikb_builder.as_markup()
