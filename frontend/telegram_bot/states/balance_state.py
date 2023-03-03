from aiogram.dispatcher.filters.state import StatesGroup, State


class BalanceStatesGroup(StatesGroup):
    WaitingPrice = State()
