Meilisearch images
##################

Running meilisearch using the command line
==========================================

It is possible to install and run a local instance of Meilisearch. Start by
installling the binaries by running:

.. code-block:: console

    curl -L https://install.meilisearch.com | sh

Once installed, run a local instance of meilisearch by running:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"
    ./meilisearch --master-key="$MEILI_MASTER_KEY"

.. note::

    Master keys for meilisearch can be generated using one of the following
    tools:

    - uuidgen
    - openssl rand
    - shasum 


For more advanced topics on how to use meilisearch, visit the `meilisearch
getting started guidelines`_.

.. _meilisearch getting started guidelines: https://www.meilisearch.com/docs/learn/getting_started/quick_start


Running meilisearch using a Docker image
========================================

A ``docker-compose.yml`` file is provided inside the ``docker/`` directory in
the `pymeilisearch repository`_.

.. _pymeilisearch repository: https://github.com/ansys/pymeilisearch

This ``docker-compose.yml`` allows to run a local instance of Meilisearch for
development purposes. The following command is used to run the image:

.. code-block:: console

    export MEILI_MASTER_KEY=$(uuidgen)
    echo "MEILI_MASTER_KEY = $MEILI_MASTER_KEY"

    docker compose run meilisearch

The application is launched in port `http://localhost:7700 <http://localhost:7700>`_
of the host machine.
