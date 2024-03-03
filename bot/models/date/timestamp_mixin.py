from dataclasses import dataclass
from datetime import datetime

from dateutil import relativedelta, tz
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..geo import Locale
from .utcnow import utcnow


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

    def created(self) -> str:
        return self.__date_diff(datetime.utcnow(), self.created_at, self.locale.time_zone)

    def updated(self) -> str:
        return self.__date_diff(datetime.utcnow(), self.updated_at, self.locale.time_zone)
