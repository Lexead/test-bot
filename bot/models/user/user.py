from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from ..geo import Locale
from .base import BaseUser


class User(BaseUser):
    __tablename__ = "users"

    language_code: Mapped[Locale] = mapped_column(Enum(Locale), default=Locale.RUSSIAN)
