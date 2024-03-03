from dataclasses import dataclass, field
from datetime import datetime, tzinfo
from typing import Any

from dateutil import relativedelta, tz


@dataclass
class DateDifference:
    left: datetime
    right: datetime
    time_zone: str | tzinfo

    def calculate(self) -> relativedelta.relativedelta:
        tz_obj = tz.gettz(self.time_zone) if isinstance(self.time_zone, str) else self.time_zone
        return relativedelta.relativedelta(self.left.astimezone(tz_obj), self.right.astimezone(tz_obj))

    def to_pretty(self) -> str:
        difference = self.calculate()

        if difference.years > 0:
            if difference.years == 1:
                return f"a year ago"
            return f"{difference.years} years ago"

        if difference.months > 0:
            if difference.months == 1:
                return f"a month ago"
            return f"{difference.months} months ago"

        if difference.days > 0:
            if difference.days == 1:
                return f"yesterday"
            return f"{difference.days} days ago"

        if difference.hours > 0:
            if difference.hours == 1:
                return f"a hour ago"
            return f"{difference.hours} hours ago"

        if difference.minutes > 0:
            if difference.minutes == 1:
                return f"a minute ago"
            return f"{difference.minutes} minutes ago"

        return f"{difference.seconds} seconds ago"
