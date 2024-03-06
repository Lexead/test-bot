from typing import TYPE_CHECKING, Sequence, TypeVar

from sqlalchemy import ColumnExpressionArgument, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .declarative import Base

ModelT = TypeVar("ModelT", bound="Base")


class BaseQueryMixin:
    @classmethod
    async def all(cls: type[ModelT], session: AsyncSession) -> Sequence[ModelT]:
        query = select(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def get(cls: type[ModelT], session: AsyncSession, *expr: bool) -> ModelT | None:
        query = select(cls).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    @classmethod
    async def filter(
        cls: type[ModelT],
        session: AsyncSession,
        *expr: ColumnExpressionArgument[bool],
        order_by: ColumnExpressionArgument[ModelT] = None,
        descending: bool = True,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[ModelT]:
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
    async def create(cls: type[ModelT], session: AsyncSession, **kwargs) -> ModelT:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        instance = cls(**kwargs)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def delete(cls: type[ModelT], session: AsyncSession, *expr: bool) -> Sequence[ModelT]:
        query = delete(cls).where(*expr).returning(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    async def delete_instance(self: ModelT, session: AsyncSession) -> None:
        await session.delete(self)

    @classmethod
    async def update(cls: type[ModelT], session: AsyncSession, *expr: bool, **kwargs) -> Sequence[ModelT]:
        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        query = update(cls).where(*expr).values(**kwargs).returning(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    async def update_instance(self: ModelT, session: AsyncSession, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        session.add(self)
        await session.flush()

    @classmethod
    async def count(cls: type[ModelT], session: AsyncSession, *expr: bool) -> int:
        query = select(func.count(cls.id)).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one()
