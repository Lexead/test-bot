from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message
from dateutil import tz
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery | InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | InlineQuery,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        user = event.from_user
        session: AsyncSession = data.get("session")

        # get user or create if not exists
        db_user = await User.get(session, User.id == user.id) or await User.create(
            session, **user.model_dump(exclude={"language_code"})
        )

        # get timezone for work with datetime
        time_zone = await db_user.get_time_zone(session)
        tz_info = tz.gettz(time_zone)

        # update user's statuses and statistics
        await db_user.update_instance(
            session,
            is_banned=(
                db_user.banned_forever
                or db_user.banned_at.astimezone(tz_info) + timedelta(seconds=db_user.banned_for)
                >= datetime.utcnow().astimezone(tz_info)
            ),
            is_removed=(
                db_user.removed_forever
                or db_user.removed_at.astimezone(tz_info) + timedelta(seconds=db_user.banned_for)
                >= datetime.utcnow().astimezone(tz_info)
            ),
        )
        await session.commit()

        # don't handle if user is banned or removed
        if db_user.is_banned or db_user.is_removed:
            return

        data["user"] = db_user
        return await handler(event, data)
