Run Meilisearch
###############

You can run Meilisearch by starting a local instance either from the
command line or from an image in a Docker container. Once the local
instance is started, yoy can test PyMeilisearch locally.

Run Meilisearch using the command line
======================================

Before you can run a local instance of Meilisearch, you must install
Meilisearch binaries with this command:

.. code-block:: console

    curl -L https://install.meilisearch.com | sh

Once the binaries are installed, start a local Meilisearch instance
with these commands:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"
    ./meilisearch --master-key="$MEILI_MASTER_KEY"


Run Meilisearch using a Docker image
====================================

In the `PyMeilisearch repository`_, the ``docker/`` directory contains the
``docker-compose.yml`` file.

.. _PyMeilisearch repository: https://github.com/ansys/pymeilisearch

This file allows you to use a Docker image to run a local instance of
Meilisearch.

To use this Docker image to start a local Meilisearch instance on the
host machine (``http://localhost:7700``), run these commands:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"

    docker compose run meilisearch

