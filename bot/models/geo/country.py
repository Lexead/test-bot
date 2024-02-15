from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(String(5), index=True)
    name: Mapped[str] = mapped_column(String(50))
