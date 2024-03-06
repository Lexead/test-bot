from datetime import datetime, tzinfo

from sqlalchemy.orm import Mapped, mapped_column

from .date_difference import DateDifference
from .utcnow import utcnow


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

    def created(self, time_zone: str | tzinfo) -> DateDifference:
        return DateDifference(datetime.utcnow(), self.created_at, time_zone)

    def updated(self, time_zone: str | tzinfo) -> DateDifference:
        return DateDifference(datetime.utcnow(), self.updated_at, time_zone)
