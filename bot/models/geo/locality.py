from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from .country import Country
from .language import Language


class Locality(Base):
    __tablename__ = "localities"

    time_zone: Mapped[str] = mapped_column(String(50), default="UTC")
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id", ondelete="cascade"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="cascade"))

    language: Mapped[Language] = relationship("Language")
    country: Mapped[Country] = relationship("Country")
