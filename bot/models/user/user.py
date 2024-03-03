from sqlalchemy import BigInteger, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from ..base import Base
from ..date import TimestampMixin
from ..geo import Locality
from .action import Action
from .role import Role
from .user_action import user_actions
from .user_role import user_roles


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), index=True)
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    is_bot: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)
    locale_id: Mapped[int | None] = mapped_column(ForeignKey("localities.id", ondelete="cascade"), nullable=True)

    full_name: Mapped[str] = column_property(f"{first_name} {last_name if last_name is not None else ''}")
    pretty_name: Mapped[str] = column_property(f"{full_name} @{username if username is not None else ''}")
