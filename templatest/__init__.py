"""Templates for testing with strings."""
from . import exceptions, templates, utils
from ._abc import BaseTemplate
from ._objects import Registered, Template
from ._version import __version__

__all__ = [
    "__version__",
    "BaseTemplate",
    "exceptions",
    "templates",
    "utils",
    "Template",
    "Registered",
]
