from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base, TimestampMixin


class BaseUser(Base, TimestampMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), index=True)
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    is_bot: Mapped[bool] = mapped_column(default=False)
    is_premium: Mapped[bool] = mapped_column(default=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

    @property
    def pretty(self) -> str:
        return f"{self.full_name} @{self.username}" if self.username else self.full_name
