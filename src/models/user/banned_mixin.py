from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..date import utcnow


class BannedMixin:
    is_banned: Mapped[bool] = mapped_column(default=False)
    banned_at: Mapped[datetime] = mapped_column(init=False, server_default=utcnow())
    banned_for: Mapped[int]
    banned_forever: Mapped[bool] = mapped_column(default=False)
