from aiogram.fsm.state import StatesGroup, State


class BalanceStatesGroup(StatesGroup):
    WAITING_PRICE = State()
