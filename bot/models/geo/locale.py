from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from .country import Country
from .language import Language


class Locale(Base):
    __tablename__ = "locale"

    time_zone: Mapped[str] = mapped_column(String(50), default="UTC")
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id", ondelete="cascade"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="cascade"))
