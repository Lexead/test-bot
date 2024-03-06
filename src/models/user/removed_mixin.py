from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..date import utcnow


class RemovedMixin:
    is_removed: Mapped[bool] = mapped_column(default=False)
    removed_at: Mapped[datetime] = mapped_column(init=False, server_default=utcnow())
    removed_for: Mapped[int]
    removed_forever: Mapped[bool] = mapped_column(default=False)
