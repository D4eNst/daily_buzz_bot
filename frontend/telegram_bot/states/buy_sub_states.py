from aiogram.dispatcher.filters.state import StatesGroup, State


class BuySubStatesGroup(StatesGroup):
    choose = State()
    confirm = State()

