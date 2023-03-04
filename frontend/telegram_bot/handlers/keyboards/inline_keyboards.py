from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import buttons
from data.config import language
from backend.database import utils as db


def list_subs() -> InlineKeyboardMarkup:
    subs = db.get_subscribes()
    ikb = InlineKeyboardMarkup()
    for sub in subs:
        ikb.add(InlineKeyboardButton(sub.title, callback_data=f"sub_{sub.sub_id}"))
    return ikb
