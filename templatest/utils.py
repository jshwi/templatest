"""
templatest.utils
================

Additional tools for working with string variables.
"""
from __future__ import annotations

import random as _random
import string as _string
import typing as _t

from typing_extensions import Self

from ._abc import MutableStrSequence as _MutableStrSequence

ALPHA = tuple(_string.ascii_uppercase)


class VarSeq(_MutableStrSequence):
    """Get string as instantiated name with the index as the suffix.

    The instantiated object will always return the same string as per
    the index. If index does not exist, strings will be generated up to
    the selected index.

    :param name: Name of the string to return.
    :param suffix: Separator between str and index.

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
        self._suffix = suffix if suffix is not None else "_"

    def __setitem__(self, i: _t.Any, o: _t.Any) -> None:
        raise NotImplementedError

    def _string(self, index: int) -> str:
        if index > len(self):
            index = len(self)

        return f"{self._name}{self._suffix}{index}"


class VarSeqSuffix(VarSeq):
    """Get string as instantiated name with the index before suffix.

    The instantiated object will always return the same string as per
    the index. If index does not exist, strings will be generated up to
    the selected index.

    :param name: Name of the string to return.
    :param suffix: Last string to return.
    :param separator: Separator between str and index.

    :example:

        >>> from templatest.utils import VarSeqSuffix
        >>> email = VarSeqSuffix("u", '@email.com')
        >>> email[0]
        'u_0@email.com'
        >>> email
        <VarSeqSuffix ['u_0@email.com']>
        >>> email[2]
        'u_2@email.com'
        >>> email
        <VarSeqSuffix ['u_0@email.com', 'u_1@email.com', 'u_2@email.com']>
    """

    def __init__(
        self, name: str, suffix: str, separator: object = None
    ) -> None:
        super().__init__(name, suffix=separator)
        self._new_suffix = suffix

    def __setitem__(self, i: _t.Any, o: _t.Any) -> None:
        raise NotImplementedError

    def _string(self, index: int) -> str:
        return f"{super()._string(index)}{self._new_suffix}"


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


class VarPrefix:
    """Get string with prefix.

    :param prefix: String to prefix attribute with.
    :param slug: Separator between words.

    :example:

        >>> from templatest.utils import VarPrefix
        >>> flag = VarPrefix("--")
        >>> slugify = VarPrefix("--", slug="-")
        >>> flag.src
        '--src'
        >>> flag.dst
        '--dst'
        >>> flag.exclude
        '--exclude'
        >>> flag
        <VarPrefix ['--src', '--dst', '--exclude']>
        >>> flag.force_remove
        '--force_remove'
        >>> slugify.force_remove
        '--force-remove'
    """

    def __init__(self, prefix: str, slug: str = "_") -> None:
        self._prefix = prefix
        self._slug = slug

    def __repr__(self) -> str:
        items = [
            i
            for i in self.__dict__.values()
            if i not in (self._prefix, self._slug)
        ]
        return f"<{self.__class__.__name__} {items}>"

    def __getattr__(self, item: str) -> str:
        while True:
            try:
                return super().__getattribute__(item)
            except AttributeError:
                self.__setattr__(
                    item, f"{self._prefix}{item.replace('_', self._slug)}"
                )


class PosArgs(_t.List[str]):
    """Get chain of strings as a list to represent positional arguments.

    :example:
        >>> from pathlib import Path
        >>> from templatest.utils import PosArgs
        >>> args = PosArgs('arg')
        Traceback (most recent call last):
        ...
        NotImplementedError: constructor cannot take args directly
        >>> other_args = PosArgs()
        >>> args = PosArgs(other_args)
        Traceback (most recent call last):
        ...
        NotImplementedError: constructor cannot take args directly
        >>> args = PosArgs()
        >>> args.path
        ['path']
        >>> args("")
        []
        >>> args("path")
        ['path']
        >>> args.path.to
        ['path', 'to']
        >>> args.path.to.another
        ['path', 'to', 'another']
        >>> args.path.to.another.path
        ['path', 'to', 'another', 'path']
        >>> args.path.to.another
        ['path', 'to', 'another']
        >>> args.path.to
        ['path', 'to']
        >>> args.path
        ['path']
        >>> args.path.another
        ['path', 'another']
        >>> args.path.another.new
        ['path', 'another', 'new']
        >>> args.path.another.new.path
        ['path', 'another', 'new', 'path']
        >>> args.src
        ['src']
        >>> args.src.to
        ['src', 'to']
        >>> args.src.to.another
        ['src', 'to', 'another']
        >>> args.src.to.another.path
        ['src', 'to', 'another', 'path']
        >>> args.src.to.another.path("")
        ['src', 'to', 'another', 'path']
        >>> args.src.to.another.path("opt")
        ['src', 'to', 'another', 'path', 'opt']
        >>> args.src.to.another.path("opt").another
        ['src', 'to', 'another', 'path', 'opt', 'another']
        >>> path = Path("/tmp")
        >>> args(path)
        ['/tmp']

    :param args: Args passed to child classes, not to be used to
        directly.
    """

    __constructor__ = True

    def __init__(self, args: _t.Any = None) -> None:
        self._isparent = True
        if isinstance(args, PosArgs) and not self.__constructor__:
            self._isparent = False
            super().__init__(args)
        elif args is not None:
            raise NotImplementedError("constructor cannot take args directly")

    def _clear_parent(self) -> None:
        if self._isparent:
            self.clear()

    def __getattr__(self, item: str) -> Self:
        self._clear_parent()
        self.append(item)
        cls = self.__class__
        cls.__constructor__ = False
        return cls(self)

    def __call__(self, arg: _t.Any) -> Self:
        self._clear_parent()
        return getattr(self, str(arg)) if arg else self
