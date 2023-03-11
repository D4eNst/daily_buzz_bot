from typing import Callable, Awaitable, Dict, Any
from aiogram.types.base import TelegramObject
from aiogram import BaseMiddleware


class CountUpdates(BaseMiddleware):
    def __init__(self):
        self.count = 0

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        # print(event)
        # print()

        self.count += 1
        if self.count > 100:
            self.count = 10
        if self.count == 1:
            return None
        else:
            return await handler(event, data)
