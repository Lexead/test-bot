from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message
from models import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery | InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | InlineQuery,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        user = event.from_user
        session: AsyncSession = data.get("session")
        db_user = await User.get(session, User.id == user.id)
        if not db_user:
            await User.create(session, **user.model_dump(exclude={"language_code"}))
            await session.commit()
        data["user"] = db_user
        return await handler(event, data)
