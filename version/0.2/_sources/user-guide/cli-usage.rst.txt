.. _cli_usage:

Scrape and upload documents or a website
########################################

You use PyMeilisearch to scrape and upload documents or a website to Meilisearch.
When starting this command-line interface (CLI) tool, you supply the template
to use for content scraping, the Meilisearch index to use for identifying content,
and the format type and location of the source documents.

.. note::
   You must declare two environment variables before using PyMeilisearch:

   - ``MEILISEARCH_HOST_URL``: Registry endpoint for Meilisearch
   - ``MEILISEARCH_API_KEY``: API key (admin) for creating indexes in the search registry


Start PyMeilisearch
===================
To start PyMeilisearch, open a command prompt or your terminal and run the
``pymeilisearch`` command followed by the desired subcommand and options.

Here is the general syntax for the ``pymeilisearch`` command:

.. code-block:: console

    $ pymeilisearch <subcommand> [options] [arguments]


**Subcommands**

The ``pymeilisearch`` command supports these subcommands:

- ``upload``: Upload documents or a website to Meilisearch.
- ``version``: Get the current version of PyMeilisearch.


Upload documents or a website
=============================

The ``upload`` subcommand uploads documents or a website to Meilisearch,
creating indexes on the Meilisearch instance.


Here is the general syntax for the ``upload`` subcommand:

.. code-block:: console

    $ pymeilisearch upload --template <template> --index <index> <source> <location> [options]

As you can see, this command requires certain arguments and supports additional options, depending
on your requirements.


**Required arguments**

- ``--template <template>``: Name of the template to use or the path to where the
  template file is located. Available templates are ``sphinx_pydata`` and ``default``.
  The Meilisearch scrapper tool, `docs-scraper <https://github.com/meilisearch/docs-scraper>`_,
  requires a configuration file to know what content to scrape. For an example of a
  configuration file, see `Set your Config File <https://github.com/meilisearch/docs-scraper#set-your-config-file>`_
  in the README for this tool's GitHub repository.
- ``--index <index name>``: Name of the Meilisearch index to use to identify content.
- ``<source>``: Format type for the documents to upload. It can be ``html``, ``url``, or ``github``.
- ``<location>``: Location of the documents or website to upload.


**Options**

- ``--cname <cname>``: CNAME that hosts the documents. While supplying a CNAME
  is optional, doing so is recommended for scraping documents on the localhost.
- ``--port <port>``: Port that the localhost is connected on. The default is ``8000``.
- ``--orgs <orgs>``: One or more GitHub organizations to scrape public GitHub pages from.


Get the PyMeilisearch version
=============================

The ``version`` command gets the version of your PyMeilisearch installation:

.. code-block:: console

    $ pymeilisearch version
