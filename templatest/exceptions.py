"""
templatest.exceptions
=====================
"""
from ._abc import BaseTemplate as _BaseTemplate


class NameConflictError(Exception):
    """Raise if non-unique :class:`templatest.BaseTemplate` name added.

    :param base_template: :class:`templatest.BaseTemplate` subclass
        which could not be registered.
    :param name: Name of :class:`templatest.BaseTemplate` subclass that
        is already registered.
    """

    def __init__(self, base_template: _BaseTemplate, name: str) -> None:
        super().__init__(
            "registered name conflict at {}: '{}'".format(
                base_template.__class__.__name__, name
            )
        )
