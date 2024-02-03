from typing import TYPE_CHECKING, Sequence, TypeVar

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .declarative import Base

T = TypeVar("T", bound="Base")


class BaseQueryMixin:
    @classmethod
    async def all(cls: type[T], session: AsyncSession) -> Sequence[T]:
        result = await session.execute(select(cls))
        return result.unique().scalars().all()

    @classmethod
    async def get_or_none(cls: type[T], session: AsyncSession, **kwargs) -> T | None:
        if id := kwargs.get("id"):
            return await session.get(cls, id)
        result = await session.execute(select(cls).filter_by(**kwargs))
        return result.scalar_one_or_none()

    @classmethod
    async def filter(
        cls: type[T],
        session: AsyncSession,
        *expr,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[T]:
        query = select(cls).where(*expr).limit(limit).offset(offset)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def create(cls: type[T], session: AsyncSession, **kwargs) -> T:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        return await session.merge(cls(**kwargs))

    @classmethod
    async def delete(cls: type[T], session: AsyncSession, *expr) -> Sequence[int]:
        return (await session.execute(delete(cls).where(*expr).returning(cls.id))).unique().scalars().all()

    async def delete_instance(self: T, session: AsyncSession) -> None:
        await session.delete(self)

    @classmethod
    async def update(cls: type[T], session: AsyncSession, *expr, **kwargs) -> Sequence[int]:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        return (
            (await session.execute(update(cls).where(*expr).values(**kwargs).returning(cls.id)))
            .unique()
            .scalars()
            .all()
        )

    async def update_instance(self: T, session: AsyncSession, **kwargs) -> None:
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        return await session.merge(self)

    @classmethod
    async def count(cls: type[T], session: AsyncSession, *expr) -> int:
        query = select(func.count(cls.id)).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one()
