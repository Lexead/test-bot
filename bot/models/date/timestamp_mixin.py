from dataclasses import dataclass
from datetime import datetime

from dateutil import relativedelta, tz
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..geo import Locale


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), init=False
    )
    locale_id: Mapped[int] = mapped_column(ForeignKey("locale.id", ondelete="cascade"))
    locale: Mapped[Locale] = relationship("Locale")

    def __date_diff(self, left: datetime, right: datetime, tz_name: str) -> str:
        tz_obj = tz.gettz(tz_name)
        date_diff = relativedelta.relativedelta(left.astimezone(tz_obj), right.astimezone(tz_obj))

        if date_diff.years > 0:
            if date_diff.years == 1:
                return f"a year ago"
            return f"{date_diff.years} years ago"

        if date_diff.months > 0:
            if date_diff.months == 1:
                return f"a month ago"
            return f"{date_diff.months} months ago"

        if date_diff.days > 0:
            if date_diff.days == 1:
                return f"yesterday"
            return f"{date_diff.days} days ago"

        if date_diff.hours > 0:
            if date_diff.hours == 1:
                return f"a hour ago"
            return f"{date_diff.hours} hours ago"

        if date_diff.minutes > 0:
            if date_diff.minutes == 1:
                return f"a minute ago"
            return f"{date_diff.minutes} minutes ago"

        return f"{date_diff.seconds} seconds ago"

    def created_diff(self) -> str:
        return self.__date_diff(datetime.utcnow(), self.created_at, self.locale.time_zone)

    def updated_diff(self) -> str:
        return self.__date_diff(datetime.utcnow(), self.updated_at, self.locale.time_zone)
