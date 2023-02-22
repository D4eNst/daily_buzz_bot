from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackStatesGroup(StatesGroup):
    WaitingText = State()
