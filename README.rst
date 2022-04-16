templatest
==========
.. image:: https://github.com/jshwi/templatest/workflows/ci/badge.svg
    :target: https://github.com/jshwi/templatest/workflows/ci/badge.svg
    :alt: ci
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/templatest
    :target: https://img.shields.io/pypi/v/templatest
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/templatest/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/templatest
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Templates for testing with strings
----------------------------------

Designed with ``pytest.mark.parametrize`` in mind

Work with subclasses inheriting from the ``templatest.BaseTemplate`` abstract base class

To use the inherited class decorate it with ``templatest.templates.register`` and ensure the module it is in is
imported at runtime

As there will be no need to import anything from this module related to this package, this can be ensured by
placing it in tests/__init__.py

.. code-block:: python

    >>> # tests/__init__.py
    >>>
    >>> import templatest
    >>>
    >>> @templatest.templates.register
    ... class _ExampleTemplate(templatest.BaseTemplate):
    ...     @property
    ...     def template(self) -> str:
    ...         return "Hello, world!"
    ...
    ...     @property
    ...     def expected(self) -> str:
    ...         return "Hello, world!"
    >>>
    >>> templatest.templates.registered.getids()
    ('example-template',)
    >>>
    >>> templatest.templates.registered.filtergroup('err').getids()
    ('example-template',)
    >>>
    >>> templatest.templates.registered.getgroup('err').getids()
    ()


The class's properties will then be available in the ``templatest.templates.registered`` object as an instance of
``templatest.Template`` named tuple

.. code-block:: python

    template = templates.templates[0]
    name = template.name
    template = template.template
    expected = template.expected

.. code-block:: python

    template = templates.templates[0]
    name, template, expected = template

Organise tests by prefixing subclasses for common tests

.. code-block:: python

    >>> # tests/__init__.py
    >>>
    >>> @templatest.templates.register
    ... class _ErrExampleTemplate(templatest.BaseTemplate):
    ...
    ...     @property
    ...     def template(self) -> str:
    ...         return "Goodbye, world..."
    ...
    ...     @property
    ...     def expected(self) -> str:
    ...         return "Goodbye, world..."
    >>>
    >>> templatest.templates.registered.getids()
    ('example-template', 'err-example-template')
    >>>
    >>> templatest.templates.registered.filtergroup('err').getids()
    ('example-template',)
    >>>
    >>> templatest.templates.registered.getgroup('err').getids()
    ('err-example-template',)

Example usage with a parametrized test
**************************************

.. code-block:: python

    >>> # tests/_test.py
    >>>
    >>> import pytest
    >>>
    >>> from templatest.templates import registered as r
    >>>
    >>> @pytest.mark.parametrize("n,t,e", r, ids=r.getids())
    ... def test_example_all(n: str, t: str, e: str) -> None: ...
    >>>
    >>> @pytest.mark.parametrize("n,t,e", r.filtergroup('err'), ids=r.filtergroup('err').getids())
    ... def test_example_no_errs(n: str, t: str, e: str) -> None: ...
    >>>
    >>> @pytest.mark.parametrize("n,t,e", r.getgroup('err'), ids=r.getgroup('err').getids())
    ... def test_example_errs(n: str, t: str, e: str) -> None:
    ...     with pytest.raises(Exception) as err:
    ...         raise Exception(e)
    ...
    ...     assert str(err.value) == e
