"""
templatest._collections
=======================
"""
from __future__ import annotations

import typing as _t

_T = _t.TypeVar("_T")


class MutableSequence(_t.MutableSequence[_T]):
    """Base mutable sequence class for all mutable sequences."""

    def __init__(self) -> None:
        self._data: _t.List[_T] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._data}>"

    def __getitem__(self, i: _t.Any) -> _t.Any:
        return self._data.__getitem__(i)

    def __setitem__(self, i: _t.Any, o: _t.Any) -> None:
        self._data.__setitem__(i, o)

    def __delitem__(self, i: _t.Any) -> None:
        self._data.__delitem__(i)

    def __len__(self) -> int:
        return self._data.__len__()

    def insert(self, index: int, value: _T) -> None:
        self._data.insert(index, value)
