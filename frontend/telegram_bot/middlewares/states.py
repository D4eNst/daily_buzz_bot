from typing import Callable, Awaitable, Dict, Any
from aiogram.fsm.context import FSMContext
from aiogram.types.base import TelegramObject
from aiogram import BaseMiddleware
from frontend.telegram_bot.states.default_state import DefaultState


class CheckStates(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        try:
            state: FSMContext = data['state']
            current_state = await state.get_state()
            if current_state is None:
                await state.set_state(DefaultState.DEFAULT_STATE)
                data['state'] = state
            # current_state = await state.get_state()
            # print(current_state)
            return await handler(event, data)
        except KeyError:
            return None
