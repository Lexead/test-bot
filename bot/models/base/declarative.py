from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from .asdict_mixin import AsDictMixin
from .query_mixin import BaseQueryMixin


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase, BaseQueryMixin, AsDictMixin):
    """Base mapped class."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, init=False)
