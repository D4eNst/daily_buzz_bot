import json
from typing import Callable, Awaitable, Dict, Any

from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram import BaseMiddleware, Bot
from frontend.bot import bot


class VerifyUser(BaseMiddleware):
    def __init__(self, redis):
        self.bot: Bot = bot
        self.redis = redis

    async def save_user_dict_to_radis(self, user_dict: dict) -> None:
        await self.redis.set('users_dict', json.dumps(user_dict))

    async def load_user_dict_from_radis(self) -> dict:
        data = await self.redis.get('users_dict')
        if data:
            return json.loads(data.decode('utf-8'))
        else:
            return {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        msg: Message = event

        self.users_dict = await self.load_user_dict_from_radis()
        if str(msg.from_user.id) not in self.users_dict:
            self.users_dict[str(msg.from_user.id)] = 0
            await self.save_user_dict_to_radis(user_dict=self.users_dict)

        try:
            command: CommandObject = data['command']
            if command.command == 'start':
                if self.users_dict[str(msg.from_user.id)] == 0:
                    self.users_dict[str(msg.from_user.id)] = 1
                    await self.save_user_dict_to_radis(user_dict=self.users_dict)
                    return await handler(event, data)
                else:
                    return await bot.send_message(msg.from_user.id,
                                                  "Please, use /start ONLY for initialize dialog with the bot")
            else:
                raise KeyError
        except KeyError:
            if self.users_dict[str(msg.from_user.id)] == 0:
                return await bot.send_message(msg.from_user.id,
                                              "Please, use /start for initialize dialog with the bot")
            else:
                return await handler(event, data)
