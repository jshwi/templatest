templatest
==========
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/templatest
    :target: https://pypi.org/project/templatest/
    :alt: PyPI
.. image:: https://github.com/jshwi/templatest/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/templatest/actions/workflows/ci.yml
    :alt: CI
.. image:: https://results.pre-commit.ci/badge/github/jshwi/templatest/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/templatest/master
   :alt: pre-commit.ci status
.. image:: https://github.com/jshwi/templatest/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/templatest/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://codecov.io/gh/jshwi/templatest/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/templatest
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/templatest/badge/?version=latest
    :target: https://templatest.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint

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
    ...         return "Hello, world"
    ...
    ...     @property
    ...     def expected(self) -> str:
    ...         return "Expected result"


The class's properties will then be available in the ``templatest.templates.registered`` object as an instance of
``templatest.Template`` named tuple

.. code-block:: python

    >>> templatest.templates.registered
    <Registered [Template(name='example-template', template='Hello, world', expected='Expected result')]>

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

``Registered.filtergroup`` can be chained, but this won't work for ``Registered.getgroup``

More succinctly, multiple prefixes can be used

.. code-block:: python

    >>> # tests/__init__.py
    >>>
    >>> @templatest.templates.register
    ... class _MultiExampleTemplate(templatest.BaseTemplate):
    ...
    ...     @property
    ...     def template(self) -> str:
    ...         return "Hello world, and goodbye world..."
    ...
    ...     @property
    ...     def expected(self) -> str:
    ...         return "Hello world, and goodbye world..."
    >>>
    >>> templatest.templates.registered.filtergroup('err').filtergroup('multi').getids()
    ('example-template',)
    >>>
    >>> templatest.templates.registered.getgroup('err').getgroup('multi').getids()
    ()
    >>>
    >>> templatest.templates.registered.filtergroup('err', 'multi').getids()
    ('example-template',)
    >>>
    >>> templatest.templates.registered.getgroup('err', 'multi').getids()
    ('err-example-template', 'multi-example-template')

Additionally, templates can be referenced by index

.. code-block::

    >>> templatest.templates.registered.getindex('example-template')
    0
    >>> templatest.templates.registered.getindex('err-example-template')
    1

.. code-block:: python

    >>> registered = templatest.templates.registered[0]
    >>> registered.name
    'example-template'
    >>> registered.template
    'Hello, world'
    >>> registered.expected
    'Expected result'

.. code-block:: python

    >>> name, template, expected = templatest.templates.registered[1]
    >>> name
    'err-example-template'
    >>> template
    'Goodbye, world...'
    >>> expected
    'Goodbye, world...'

And a template can be returned by name

.. code-block::

    >>> templatest.templates.registered.getbyname('example-template')
    Template(name='example-template', template='Hello, world', expected='Expected result')
    >>> templatest.templates.registered.getbyname('err-example-template')
    Template(name='err-example-template', template='Goodbye, world...', expected='Goodbye, world...')

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
