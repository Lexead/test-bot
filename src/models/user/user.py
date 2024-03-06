from typing import Any, Sequence

from sqlalchemy import BigInteger, ForeignKey, String, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, column_property, mapped_column

from ..base import Base
from ..date import TimestampMixin
from ..geo import Country, Language, Locality
from .action import Action
from .banned_mixin import BannedMixin
from .removed_mixin import RemovedMixin
from .role import Role
from .role_action import RoleAction
from .user_action import UserAction
from .user_role import UserRole


class User(Base, TimestampMixin, BannedMixin, RemovedMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), index=True)
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    is_bot: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)

    locality_id: Mapped[int | None] = mapped_column(ForeignKey("localities.id", ondelete="cascade"), nullable=True)

    full_name: Mapped[str] = column_property(f"{first_name} {last_name if last_name is not None else ''}")
    pretty_name: Mapped[str] = column_property(f"{full_name} @{username if username is not None else ''}")

    async def get_language(self, session: AsyncSession) -> Language | None:
        if self.locality_id is None:
            return None
        query = (
            select(Language).join(Locality, Language.id == Locality.language_id).where(Locality.id == self.locality_id)
        )
        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_time_zone(self, session: AsyncSession) -> str:
        if self.locality_id is None:
            return "UTC"
        query = select(Locality.time_zone).where(Locality.id == self.locality_id)
        result = await session.execute(query)
        return result.unique().scalar_one()

    async def get_roles(self, session: AsyncSession) -> Sequence[Role]:
        query = select(Role).join(UserRole, Role.id == UserRole.role_id).where(UserRole.user_id == self.id)
        result = await session.execute(query)
        return result.unique().scalars().all()

    async def get_actions(self, session: AsyncSession) -> Sequence[Action]:
        user_query = (
            select(Action).join(UserAction, Action.id == UserAction.action_id).where(UserAction.user_id == self.id)
        )
        role_query = (
            select(Action)
            .join(RoleAction, Action.id == RoleAction.action_id)
            .join(Role, RoleAction.role_id == Role.id)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == self.id)
        )
        query = select(Action).from_statement(union_all(user_query, role_query))
        result = await session.execute(query)
        return result.unique().scalars().all()
