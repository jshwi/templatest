"""
templatest._abc
===============
"""
from __future__ import annotations

import re as _re
import typing as _t
from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod

from ._collections import MutableSequence as _MutableSequence


class MutableStrSequence(_MutableSequence[str]):
    """Base class for mutable sequences of dynamically created strs."""

    @_abstractmethod
    def _string(self, index: int) -> str:
        """Method to create and append new string.

        The string produced will be created up until the index provided.
        """

    def __getitem__(self, index: _t.Any) -> _t.Any:
        if isinstance(index, slice):
            return super().__getitem__(index)

        while True:
            try:
                return super().__getitem__(index)
            except IndexError:
                self.append(self._string(index))


class BaseTemplate(_ABC):
    """Abstract base class for string template and expected tests.

    Override the :meth:`template` abstract property method with a string
    that the test will be working with.

    Override the :meth:`expected` abstract property method with the
    expected result that the test will produce.
    """

    def __init__(self) -> None:
        by_caps = "-".join(
            i.lower()
            for i in _re.findall("[A-Z][^A-Z]*", self.__class__.__name__)
        )
        string = ""
        for char in by_caps:
            if char.isdigit():
                char = f"-{char}-"

            string += char

        if string.endswith("-"):
            string = string[:-1]

        string = string.replace("_", "-")
        self._name = string.replace("--", "-")

    @property
    def name(self) -> str:
        """The name of the inherited class, parsed for test ID."""
        return self._name

    @property
    @_abstractmethod
    def template(self) -> str:
        """Template to test."""

    @property
    @_abstractmethod
    def expected(self) -> str:
        """Expected result."""
