"""
templatest.templates
====================

Registration and usage of template subclasses.
"""
import typing as _t

from ._abc import BaseTemplate as _BaseTemplate
from ._objects import Registered as _Registered
from ._objects import Template as _Template
from .exceptions import NameConflictError as _NameConflictError

#: Instantiated :class:`templatest.Registered` object for accessing
#: :class:`templatest.Template` properties
#:
#: Populated through registering :class:`templatest.BaseTemplate`
#: subclasses with :func:`register`.
registered = _Registered()


def register(base_template: _t.Type[_BaseTemplate]) -> _t.Type[_BaseTemplate]:
    """Register :class:`templatest.BaseTemplate` subclasses.

    Decorate subclass definition to register.

    Registered subclasses of :class:`templatest.BaseTemplate` can be
    accessed through :attr:`registered`.

    :param base_template: :class:`templatest.BaseTemplate` object.
    :return: :class:`templatest.BaseTemplate` object.
    """
    inst = base_template()
    for template in registered:
        if inst.name == template.name:
            raise _NameConflictError(inst, inst.name)

    registered.append(_Template(inst.name, inst.template, inst.expected))
    return base_template
