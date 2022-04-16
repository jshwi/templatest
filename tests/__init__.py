"""
tests
=====
"""
# pylint: disable=too-few-public-methods
import typing as t

from templatest.utils import VarSeq

TEST_CLASS_NAME = VarSeq("_TestTemplate")
TEST_ERR_CLASS_NAME = VarSeq("_ErrTestTemplate")
TEST_INST_NAME = VarSeq("test-template", suffix="-")
TEST_ERR_INST_NAME = VarSeq("err-test-template", suffix="-")

RegisterTemplatesType = t.Callable[..., None]


class RegisterTemplateType(t.Protocol):
    """Return type for ``fixture_register_template``."""

    def __call__(
        self,
        name: str,
        template: t.Optional[str] = None,
        expected: t.Optional[str] = None,
    ) -> None:
        """No __call__ method implemented."""
