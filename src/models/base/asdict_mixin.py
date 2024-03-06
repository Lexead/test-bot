from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .declarative import Base

T = TypeVar("T", bound="Base")


class AsDictMixin:
    def as_dict(self: T, *excluded_columns: str) -> dict:
        return {k: v for k, v in self.__table__.columns.items() if not k in excluded_columns}
