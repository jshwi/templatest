"""
tests
=====
"""
# pylint: disable=protected-access
import typing as t

import pytest

import templatest

from . import (
    TEST_CLASS_NAME,
    TEST_ERR_CLASS_NAME,
    TEST_ERR_INST_NAME,
    TEST_INST_NAME,
    RegisterTemplatesType,
    RegisterTemplateType,
)


def test_var_seq() -> None:
    """Test ``VarSeq``."""
    const = templatest.utils.VarSeq("CONST")
    assert const[0] == "CONST_0"
    assert str(const) == "<VarSeq ['CONST_0']>"
    assert const[1] == "CONST_1"
    assert str(const) == "<VarSeq ['CONST_0', 'CONST_1']>"
    assert const[4] == "CONST_4"
    assert (
        str(const)
        == "<VarSeq ['CONST_0', 'CONST_1', 'CONST_2', 'CONST_3', 'CONST_4']>"
    )
    assert const[1:3] == ["CONST_1", "CONST_2"]
    with pytest.raises(NotImplementedError):
        const[4] = "CUSTOM_CONST"


def test_rand_str_len_seq() -> None:
    """Test ``RandStrLenSeq``."""
    len_3 = templatest.utils.RandStrLenSeq(3)
    assert len(len_3) == 0
    str_1 = len_3[0]
    assert isinstance(str_1, str)
    assert len(len_3) == 1
    assert len(str_1) == 3
    str_2 = len_3[1]
    assert len(len_3) == 2
    assert str_1 != str_2
    with pytest.raises(NotImplementedError):
        len_3[1] = "custom_str"


def test_register_template(register_template: RegisterTemplateType) -> None:
    """Test registering a :class:`templatest.BaseTemplate` subclass.

    :param register_template: Register a test subclass of
        :class:`templatest.BaseTemplate`.
    """
    strings = templatest.utils.RandStrLenSeq(3)
    register_template(TEST_CLASS_NAME[0], strings[0], strings[1])
    template = templatest.templates.registered[0]
    assert template.name == TEST_INST_NAME[0]
    assert template.template == strings[0]
    assert template.expected == strings[1]


def test_name_conflict_error(register_template: RegisterTemplateType) -> None:
    """Test registering a :class:`templatest.BaseTemplate` name
    conflict.

    :param register_template: Register a test subclass of
        :class:`templatest.BaseTemplate`.
    """
    register_template(TEST_CLASS_NAME[0])
    with pytest.raises(templatest.exceptions.NameConflictError) as err:
        register_template(TEST_CLASS_NAME[0])

    assert str(err.value) == (
        f"registered name conflict at"
        f" {TEST_CLASS_NAME[0]}: '{TEST_INST_NAME[0]}'"
    )


def test_get_ids(register_templates: RegisterTemplatesType) -> None:
    """Test :meth:`Templates.getids` method.

    :param register_templates: Register any number of test subclasses of
        :class:`templatest.BaseTemplate`
    """
    register_templates(
        (TEST_CLASS_NAME[0],), (TEST_CLASS_NAME[1],), (TEST_CLASS_NAME[2],)
    )
    assert templatest.templates.registered.getids() == (
        TEST_INST_NAME[0],
        TEST_INST_NAME[1],
        TEST_INST_NAME[2],
    )


def test_get_group(register_templates: RegisterTemplatesType) -> None:
    """Test ``Templates.getgroup`` method.

    :param register_templates: Register any number of test subclasses of
        ``BaseTemplate.``
    """
    register_templates(
        (TEST_CLASS_NAME[0],), (TEST_CLASS_NAME[1],), (TEST_CLASS_NAME[2],)
    )
    register_templates(
        (TEST_ERR_CLASS_NAME[0],),
        (TEST_ERR_CLASS_NAME[1],),
        (TEST_ERR_CLASS_NAME[2],),
    )
    assert templatest.templates.registered.getgroup("err").getids() == (
        TEST_ERR_INST_NAME[0],
        TEST_ERR_INST_NAME[1],
        TEST_ERR_INST_NAME[2],
    )


def test_filter_group(register_templates: RegisterTemplatesType) -> None:
    """Test ``Templates.filtergroup`` method.

    :param register_templates: Register any number of test subclasses of
        ``BaseTemplate.``
    """
    register_templates(
        (TEST_CLASS_NAME[0],), (TEST_CLASS_NAME[1],), (TEST_CLASS_NAME[2],)
    )
    register_templates(
        (TEST_ERR_CLASS_NAME[0],),
        (TEST_ERR_CLASS_NAME[1],),
        (TEST_ERR_CLASS_NAME[2],),
    )
    assert templatest.templates.registered.filtergroup("err").getids() == (
        TEST_INST_NAME[0],
        TEST_INST_NAME[1],
        TEST_INST_NAME[2],
    )


def test_mutable_mapping_setitem() -> None:
    """Get coverage on setitem."""
    # noinspection PyUnresolvedReferences
    seq: t.MutableSequence = templatest._collections.MutableSequence()
    seq.append(templatest.utils.ALPHA[0])
    assert str(seq) == f"<MutableSequence ['{templatest.utils.ALPHA[0]}']>"
    seq[0] = templatest.utils.ALPHA[1]
    assert str(seq) == f"<MutableSequence ['{templatest.utils.ALPHA[1]}']>"


def test_get_index(register_templates: RegisterTemplatesType) -> None:
    """Test :meth:`Templates.getindex` method.

    :param register_templates: Register any number of test subclasses of
        :class:`templatest.BaseTemplate`
    """
    register_templates(
        (TEST_CLASS_NAME[0],), (TEST_CLASS_NAME[1],), (TEST_CLASS_NAME[2],)
    )
    assert templatest.templates.registered.getindex(TEST_INST_NAME[0]) == 0
    assert templatest.templates.registered.getindex(TEST_INST_NAME[1]) == 1
    assert templatest.templates.registered.getindex(TEST_INST_NAME[2]) == 2
    assert templatest.templates.registered.getindex(TEST_INST_NAME[3]) is None
