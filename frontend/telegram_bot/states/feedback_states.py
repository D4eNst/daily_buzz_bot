from aiogram.fsm.state import StatesGroup, State


class FeedbackStatesGroup(StatesGroup):
    WAITING_TEXT = State()
