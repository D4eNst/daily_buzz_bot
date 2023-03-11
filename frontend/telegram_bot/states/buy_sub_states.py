from aiogram.fsm.state import StatesGroup, State


class BuySubStatesGroup(StatesGroup):
    CHOOSE = State()
    CONFIRM = State()

