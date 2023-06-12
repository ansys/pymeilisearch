pymeilisearch
=======================
|python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |python| image:: https://img.shields.io/pypi/pyversions/pymeilisearch?logo=pypi
   :target: https://pypi.org/project/pymeilisearch/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/pymeilisearch.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/pymeilisearch
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/ansys/pymeilisearch/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pymeilisearch
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/pymeilisearch/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pymeilisearch/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


The PyMeilisearch CLI is a command-line interface utility for interacting with MeiliSearch, 
an open-source search engine. It provides convenient commands for uploading files or websites to MeiliSearch indexes.


How to install
--------------

At least two installation modes are provided: user and developer.

For users
^^^^^^^^^

In order to install PyMeilisearch, make sure you
have the latest version of `pip`_. To do so, run:

.. code:: bash

    python -m pip install -U pip

Then, you can simply execute:

.. code:: bash

    python -m pip install pymeilisearch

For developers
^^^^^^^^^^^^^^

Installing PyMeilisearch in developer mode allows
you to modify the source and enhance it.

Before contributing to the project, please refer to the `PyAnsys Developer's guide`_. You will 
need to follow these steps:

#. Start by cloning this repository:

   .. code:: bash

      git clone https://github.com/ansys/pymeilisearch

#. Create a fresh-clean Python environment and activate it:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure you have the latest required build system and doc, testing, and CI tools:

   .. code:: bash

      python -m pip install -U pip flit tox


#. Install the project in editable mode:

    .. code:: bash
    
      python -m pip install --editable pymeilisearch
    
    #. Finally, verify your development installation by running:

   .. code:: bash
        
      tox

Highlights
----------

MeiliSearch is an open-source search engine designed for developers to integrate into their applications.
It offers fast and relevant search capabilities for handling large amounts of textual data.
MeiliSearch focuses on simplicity and ease of use while delivering high performance and accurate search results.

PyMeilisearch CLI is a command-line interface tool for MeiliSearch, built on top of the 
PyMeilisearch Python client library. It provides a convenient way for developers to 
interact with MeiliSearch from the command line, enabling them to perform operations such as indexing, 
searching, updating, and deleting documents.


Overview of Features
--------------------

#. *Easy integration*: PyMeilisearch simplifies the integration of MeiliSearch into Python projects without custom code.
   (see `user_guide`_)

#. *High-level functionality*: PyMeilisearch provides functions for indexing data, performing searches, 
   and managing documents, abstracting away complexity.

#. *Flexibility and customization*: PyMeilisearch allows customization of search parameters, 
   filtering options, and indexing configurations for tailored search experiences.(see `getting_started`_)

By combining MeiliSearch's powerful search capabilities with the simplicity and convenience of PyMeilisearch, 
developers can enhance their applications with efficient and accurate search functionality.

How to testing
--------------

This project takes advantage of `tox`_. This tool allows to automate common
development tasks (similar to Makefile) but it is oriented towards Python
development. 

Using tox
^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment so anything being tested is isolated from the project in
order to guarantee project's integrity. The following environments commands are provided:

- **tox -e style**: will check for coding style quality.
- **tox -e py**: checks for unit tests.
- **tox -e py-coverage**: checks for unit testing and code coverage.
- **tox -e doc**: checs for documentation building process.


Raw testing
^^^^^^^^^^^

If required, you can always call the style commands (`black`_, `isort`_,
`flake8`_...) or unit testing ones (`pytest`_) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


A note on pre-commit
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool via:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

Refer to the `documentation <http://pymeilisearch.docs.ansys.com/>`_ for detailed
installation and usage details.

For general questions about the project, its applications, or about cli
usage, please create a discussion in `pymeilisearch/discussions`_
where the contributors can collectively address your questions.

.. _pymeilisearch/discussions: https://github.com/ansys/pymeilisearch/discussions

Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt
    python -m build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
.. _getting_started: https://pymeilisearch.docs.ansys.com/version/stable/getting-started/index.html
.. _user_guide: https://pymeilisearch.docs.ansys.com/version/dev/user-guide/index.html
