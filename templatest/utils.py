"""
templatest.utils
================

Additional tools for working with string variables.
"""
from __future__ import annotations

import random as _random
import string as _string
import typing as _t

from ._abc import MutableStrSequence as _MutableStrSequence

ALPHA = tuple(_string.ascii_uppercase)


class VarSeq(_MutableStrSequence):
    """Get string as instantiated name with the index as the suffix.

    The instantiated object will always return the same string as per
    the index. If index does not exist, strings will be generated up to
    the selected index.

    :param name: Name of the string to return.
    :param suffix: Seperator between str and index.

    :example:

        >>> from templatest.utils import VarSeq
        >>> CONST = VarSeq("CONST")
        >>> CONST[0]
        'CONST_0'
        >>> CONST
        <VarSeq ['CONST_0']>
        >>> CONST[1]
        'CONST_1'
        >>> CONST
        <VarSeq ['CONST_0', 'CONST_1']>
        >>> CONST[4]
        'CONST_4'
        >>> CONST
        <VarSeq ['CONST_0', 'CONST_1', 'CONST_2', 'CONST_3', 'CONST_4']>
        >>> name = VarSeq("package-name", suffix="-")
        >>> name[0]
        'package-name-0'
    """

    def __init__(self, name: str, suffix: object = None) -> None:
        super().__init__()
        self._name = name
        self._suffix = suffix or "_"

    def __setitem__(self, i: _t.Any, o: _t.Any) -> None:
        raise NotImplementedError

    def _string(self, index: int) -> str:
        if index > len(self):
            index = len(self)

        return f"{self._name}{self._suffix}{index}"


class RandStrLenSeq(_MutableStrSequence):
    """Get random string of varying length.

    The instantiated object will always return the same string as per
    the index. If index does not exist, strings will be generated up to
    the selected index.

    :param length: Length of string.

    :example:

        >>> from templatest.utils import RandStrLenSeq
        >>> LEN_3 = RandStrLenSeq(3)
        >>> len(LEN_3)
        0
        >>> str_1 = LEN_3[0]
        >>> type(str_1)
        <class 'str'>
        >>> len(str_1)
        3
        >>> len(LEN_3)
        1
        >>> str_2 = LEN_3[1]
        >>> len(LEN_3)
        2
        >>> assert str_1 != str_2
    """

    def __setitem__(self, i: _t.Any, o: _t.Any) -> None:
        raise NotImplementedError

    def __init__(self, length: int) -> None:
        super().__init__()
        self._len = length

    def _string(self, index: int) -> str:
        return "".join(_random.choices(_string.ascii_lowercase, k=self._len))
