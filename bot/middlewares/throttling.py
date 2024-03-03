from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, InlineQuery, Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery | InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | InlineQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user
        check_user = await self.storage.redis.get(name=str(user.id))

        if check_user is not None:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=str(user.id), value=0, ex=10)
                return await event.answer("Мы обнаружили подозрительную активность. Ждите 10 секунд.")
            return
        await self.storage.redis.set(name=str(user.id), value=1, ex=10)

        return await handler(event, data)
