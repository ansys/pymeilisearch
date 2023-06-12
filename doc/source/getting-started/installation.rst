Installation
============
The pymeilisearch package currently supports Python 3.7 through Python 3.11 on Windows, Mac OS, and Linux.

How to install
--------------

At least two installation modes are provided: user and developer.

Install the latest release from PyPi with:

    python -m pip install pymeilisearch

Alternatively, install the latest from PyMeilisearch GitHub via:

    pip install git+https://github.com/ansys/pymeilisearch.git

For a local development version, install with:

#. Start by cloning this repository:

   .. code:: bash

      git clone https://github.com/ansys-internal/pymeilisearch

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

Offline installation
--------------------

If you lack an internet connection on your install machine, the recommended way of installing Pymeilisearch is downloading the wheelhouse 
archive from the `Releases Page <https://github.com/ansys/pymeilisearch/releases>` for your corresponding machine architecture.

Each wheelhouse archive contains all the Python wheels necessary to install PyMeilisearch from scratch on Windows and Linux for Python 3.7.
You can install this on an isolated system with a fresh Python or on a virtual environment.

For example, on Linux with Python 3.7, unzip it and install it with the following:

.. code:: bash

    unzip ansys_tools_meilisearch-0.1.6-py3-none-any wheelhouse
    pip install pymeilisearch -f wheelhouse --no-index --upgrade --ignore-installed

