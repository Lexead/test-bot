from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Action(Base):
    __tablename__ = "actions"

    type: Mapped[str] = mapped_column(String(50))
    object: Mapped[str] = mapped_column(String(100))
