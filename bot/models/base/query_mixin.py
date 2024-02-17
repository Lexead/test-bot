from typing import TYPE_CHECKING, Sequence, TypeVar

from sqlalchemy import ColumnElement, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .declarative import Base

T = TypeVar("T", bound="Base")


class BaseQueryMixin:
    @classmethod
    async def all(cls: type[T], session: AsyncSession) -> Sequence[T]:
        query = select(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def get(cls: type[T], session: AsyncSession, *expr: bool) -> T | None:
        query = select(cls).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    @classmethod
    async def filter(
        cls: type[T],
        session: AsyncSession,
        *expr: bool,
        order_by: ColumnElement[T] = None,
        descending: bool = True,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[T]:
        query = select(cls).where(*expr)
        if order_by is not None:
            order = desc if descending else asc
            query = query.order_by(order(order_by))
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def create(cls: type[T], session: AsyncSession, **kwargs) -> None:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        session.add(cls(**kwargs))

    @classmethod
    async def delete(cls: type[T], session: AsyncSession, *expr: bool) -> Sequence[T]:
        query = delete(cls).where(*expr).returning(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    async def delete_instance(self: T, session: AsyncSession) -> None:
        await session.delete(self)

    @classmethod
    async def update(cls: type[T], session: AsyncSession, *expr: bool, **kwargs) -> Sequence[T]:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        query = update(cls).where(*expr).values(**kwargs).returning(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    async def update_instance(self: T, session: AsyncSession, **kwargs) -> None:
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        session.add(self)

    @classmethod
    async def count(cls: type[T], session: AsyncSession, *expr: bool) -> int:
        query = select(func.count(cls.id)).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one()
