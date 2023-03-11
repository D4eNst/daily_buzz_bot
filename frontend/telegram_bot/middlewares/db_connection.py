import asyncpg
from typing import Callable, Awaitable, Dict, Any
from aiogram.types.base import TelegramObject
from backend.database.utils import Database
from aiogram import BaseMiddleware


class DbSession(BaseMiddleware):
    def __init__(self, conn: asyncpg.pool.Pool):
        self.connector = conn
        super(DbSession, self).__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.connector.acquire() as connect:
            data['db'] = Database(connect)
            return await handler(event, data)
