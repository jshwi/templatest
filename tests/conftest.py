"""
tests.conftest
==============
"""
from __future__ import annotations

import typing as t

import pytest

import templatest

from . import RegisterTemplatesType, RegisterTemplateType


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment() -> None:
    """Ensure :attr:`templatest.templates.registered` resets."""
    templatest.templates.registered.clear()


@pytest.fixture(name="register_template")
def fixture_register_template() -> RegisterTemplateType:
    """Register a test subclass of :class:`templatest.BaseTemplate`.

    :return: Function for using this fixture.
    """

    def _register_template(
        name: str, template: str | None = None, expected: str | None = None
    ) -> None:
        class _TestTemplate(templatest.BaseTemplate):
            @property
            def template(self) -> str:
                return template or ""

            @property
            def expected(self) -> str:
                return expected or ""

        _TestTemplate.__name__ = name
        templatest.templates.register(_TestTemplate)

    return _register_template


@pytest.fixture(name="register_templates")
def fixture_register_templates(
    register_template: RegisterTemplatesType,
) -> t.Callable[..., None]:
    """Register any number of :class:`templatest.BaseTemplate`
    subclasses.

    :param register_template: Register a test subclass of
        :class:`templatest.BaseTemplate`.
    :return: Function for using this fixture.
    """

    def _register_templates(*args: t.Tuple[str, str, str]) -> None:
        for arg in args:
            register_template(*arg)

    return _register_templates
