from datetime import datetime

from dateutil import relativedelta, tz
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), init=False
    )

    def __pretty(self, left_dt: datetime, right_dt: datetime, tz_name: str) -> str:
        tz_obj = tz.gettz(tz_name)
        date_diff = relativedelta.relativedelta(left_dt.astimezone(tz_obj), right_dt.astimezone(tz_obj))

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

    def created_pretty(self, tz_name: str) -> str:
        return self.__pretty(datetime.utcnow(), self.created_at, tz_name)

    def updated_pretty(self, tz_name: str) -> str:
        return self.__pretty(datetime.utcnow(), self.updated_at, tz_name)
