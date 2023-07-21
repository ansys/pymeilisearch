Installing pymeilisearch
########################

Installing ``pymeilisearch`` is as simple as installing a Python library.
However, users, and developers need to host a `Meilisearch`_ service to upload
the desired documentation indices.

.. _meilisearch: https://www.meilisearch.com/


User installation
=================

There are multiple sources for installing the latest stable version of
``pymeilisearch``. These include ``pip`` and ``GitHub``.


.. jinja:: install_guide

    .. tab-set::

        .. tab-item:: Public PyPI

            .. code-block:: console

                python -m pip install pymeilisearch


        .. tab-item:: Private PyPI

            .. code-block:: console

                export TWINE_USERNAME="__token__"
                export TWINE_REPOSITORY_URL="https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/upload"
                export TWINE_PASSWORD=***
                python -m pip install pymeilisearch


        .. tab-item:: GitHub

            .. code-block:: console

                python -m pip install git+https://github.com/ansys/pymeilisearch.git@v{{ version }}


Developer installation
======================

The developer installation is specifically intended for project maintainers.
This specialized installation is tailored to equip developers with the essential
tools and resources required for effective contribution to the project's
development and maintenance. The developer installation assumes a certain level
of technical expertise and familiarity with the project's codebase, rendering it
most suitable for individuals actively engaged in its continuous development and
maintenance.

Start by cloning the repository

.. code-block::

    git clone git@github.com:ansys/pymeilisearch


Move inside the project and create a new Python environment:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    py -m venv <venv>

            .. tab-item:: PowerShell

                .. code-block:: text

                    py -m venv <venv>

    .. tab-item:: Linux/UNIX

        .. code-block:: text

            python -m venv <venv>

Activate previous environment:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    <venv>\Scripts\activate.bat

            .. tab-item:: PowerShell

                .. code-block:: text

                    <venv>\Scripts\Activate.ps1

    .. tab-item:: Linux/UNIX

        .. code-block:: text

            source <venv>/bin/activate

Install the project in editable mode. This means that any changes you make to
the package's source code immediately reflect in your project without requiring
to reinstalling it.

.. code-block::

    python -m pip install --editable .
