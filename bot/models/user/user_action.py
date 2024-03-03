from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class UserAction(Base):
    __tablename__ = "user_actions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id", ondelete="cascade"), primary_key=True)
