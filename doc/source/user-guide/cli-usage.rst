Using pymeilisearch CLI utility
###############################

To use the CLI tool, open your terminal or command prompt and run the
`pymeilisearch` command, followed by the desired sub-command and options.

General syntax:

.. code-block:: console

    $ pymeilisearch <sub-command> [options] [arguments]

Previous command expects two environment variables to be declared:

- ``MEILISEARCH_HOST_URL`` is used to indicate the registry endpoint
- ``MEILISEARCH_API_KEY`` is used to create new indices into the search registry


Available commands
==================

The ``pymeilisearch`` command provides the following sub-commands:

- ``upload`` is used to create new indices on a ``meilisearch`` instance
- ``version`` is used to return the current version of ``pymeilisearch``


The ``upload`` command
----------------------

The ``upload`` sub-command allows you to upload files or a website to Meilisearch.
It supports different sources and options depending on your requirements.

Syntax:

.. code-block:: console

    $ pymeilisearch upload --template <template> --index <index> <source> <location> [options]

Required arguments:

- ``--template <template name or path>`` indicates the Name of the template to use or specify the path where the template is located. 
    Available templates are `sphinx_pydata` and `default`. The `config file` required to know which content you want to scrape.
    The example `config files` available in `meilisearch-docs-scrapper`_.

.. _meilisearch-docs-scrapper: https://github.com/meilisearch/docs-scraper#set-your-config-file

- ``--index <index name>`` indicates the name of the Meilisearch index used to identify the content.
- ``<source>`` is the type source to upload. It can be ``html``, ``url``, or ``github``.
- ``<location>`` indicates the location of the files or website to upload.

Options:

- ``--cname <cname>`` is the CNAME in which the documents are hosted (optional), recommended for localhost scraping.
- ``--port <port>`` is the number for the port in which the local host has to connect. Default port is 8000.
- ``--orgs <orgs>`` is the name for the GitHub organizations from which public GitHub pages get scraped.


The ``version`` command
-----------------------

The ``version`` command displays the current version of the ``pymeilisearch``:

Syntax:

.. code-block:: console

    $ pymeilisearch version
