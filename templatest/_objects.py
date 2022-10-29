"""
templatest._objects
===================
"""
from __future__ import annotations

import typing as _t

from ._collections import MutableSequence as _MutableSequence


class Template(_t.NamedTuple):
    """Contains registered :class:`BaseTemplate` properties."""

    #: The name of the inherited class, parsed for test ID.
    name: str

    #: Template to test.
    template: str

    #: Expected result.
    expected: str


class Registered(_MutableSequence[Template]):
    """Mutable sequence of :class:`Template` named tuples.

    :param args: Instantiate with any number of :class:`Template`
        objects.
    """

    def __init__(self, *args: Template) -> None:
        super().__init__()
        self.extend(args)

    def filtergroup(self, *prefix: str) -> Registered:
        """Get new object excluding templates sharing a prefix.

        :param prefix: Common prefix(s) to registered subclasses.
        :return: New :class:`Registered` object containing
            :class:`Template` objects that do not have the provided
            prefix in their names.
        """
        return Registered(
            *(x for x in self if not any(x.name.startswith(y) for y in prefix))
        )

    def getgroup(self, *prefix: str) -> Registered:
        """Get new object containing templates sharing a prefix.

        :param prefix: Common prefix(s) to registered subclasses.
        :return: New :class:`Registered` object containing
            :class:`Template` objects with common prefix to their names.
        """
        return Registered(
            *(x for y in prefix for x in self if x.name.startswith(y))
        )

    def getids(self) -> _t.Tuple[str, ...]:
        """Returns a tuple of all the names of the classes contained.

        :return: A tuple of names of the classes within this sequence.
        """
        return tuple(i.name for i in self)

    def getbyname(self, name: str) -> Template | None:
        """Get a template by name if it exists.

        :param name: Name assigned to template.
        :return: :class:`Template` object.
        """
        return next((i for i in self if i.name == name), None)

    def getindex(self, name: str) -> int | None:
        """Get the index of a template by name if it exists.

        :param name: Name assigned to template.
        :return: Index of the template if it exists, else None.
        """
        template = self.getbyname(name)
        return template if template is None else self.index(template)
