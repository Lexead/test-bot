from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class RoleAction(Base):
    __tablename__ = "role_actions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="cascade"), primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id", ondelete="cascade"), primary_key=True)
