Run Meilisearch
###############

You can run a local instance of Meilisearch either from the
command line or from an image in a Docker container.

.. note::

    Both methods of running a local instance of Meilisearch require
    a master key. To generate a master key, you can use one of
    these tools:

    - `UUID Generator <https://uuidgen.org/v/4>`_
    - `OpenSSL <https://www.openssl.org/docs/man1.1.1/man1/rand.html>`_
    - `shasum <https://linux.die.net/man/1/shasum>`_


For more information, see the `Meilisearch Quick Start`_.

.. _Meilisearch Quick Start: https://www.meilisearch.com/docs/learn/getting_started/quick_start


Run Meilisearch from the command line
======================================

On the command line, first install the Meilisearch binaries with
this command:

.. code-block:: console

    curl -L https://install.meilisearch.com | sh

Once these binaries are installed, start a local instance of
Meilisearch with these commands:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"
    ./meilisearch --master-key="$MEILI_MASTER_KEY"


Run Meilisearch from a Docker image
===================================

In the `PyMeilisearch repository`_, the ``docker/`` directory  contains a
``docker-compose.yml`` file.

.. _PyMeilisearch repository: https://github.com/ansys/pymeilisearch

You can use this YML file to run Meilisearch from this Docker image
for development purposes.

To run this Docker image, use these commands:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"

    docker compose run meilisearch

The service launches on port `http://localhost:7700 <http://localhost:7700>`_
of the host machine. You can now use this Docker image to test PyMeilisearch
locally.
