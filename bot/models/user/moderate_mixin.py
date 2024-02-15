from typing import TYPE_CHECKING, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from .base import BaseUser

UserT = TypeVar("UserT", bound="BaseUser")


class ModerateMixin:
    banned: Mapped[bool] = mapped_column(default=False)
    verified: Mapped[bool] = mapped_column(default=False)

    async def ban(self, session: AsyncSession, unban: bool = False):
        self.banned = not unban
        await session.merge(self)

    async def verify(self, session: AsyncSession, unverify: bool = False):
        self.verified = not unverify
        await session.merge(self)
