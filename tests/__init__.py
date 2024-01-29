"""
tests
=====
"""

# pylint: disable=too-few-public-methods
from __future__ import annotations

import typing as t

from templatest.utils import VarSeq

TEST_CLASS_NAME = VarSeq("_TestTemplate")
TEST_ERR_CLASS_NAME = VarSeq("_ErrTestTemplate")
TEST_MULTI_CLASS_NAME = VarSeq("_MultiTestTemplate")
TEST_INST_NAME = VarSeq("test-template", suffix="-")
TEST_ERR_INST_NAME = VarSeq("err-test-template", suffix="-")
TEST_MULTI_INST_NAME = VarSeq("multi-test-template", suffix="-")

MULTI = "multi"
TEST = "test"
ERROR = "err"
VERSION = "0.1.0"

RegisterTemplatesType = t.Callable[..., None]


class RegisterTemplateType(t.Protocol):
    """Return type for ``fixture_register_template``."""

    def __call__(
        self,
        name: str,
        template: str | None = None,
        expected: str | None = None,
    ) -> None:
        """No __call__ method implemented."""
