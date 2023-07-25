Scrape and upload documents or a website
########################################

You use PyMeilisearch to scrape and upload documents or a website to Meilisearch.
When starting this command-line interface (CLI) tool, you supply the template
to use for content scraping, the Meilisearch index to use for identifying content,
and the format type and location of the source documents.

.. note::
   You must declare two environment variables before using PyMeilisearch:

   - ``MEILISEARCH_HOST_URL``: Registry endpoint for Meilisearch
   - ``MEILISEARCH_API_KEY``: API key for creating indexes in the search registry


Start PyMeilisearch
===================
To start PyMeilisearch, open your terminal or command prompt and run the
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

The ``upload`` subcommand uploads docouments or a website to Meilisearch,
creating indexes on the Meilisearch instance.


Here is the general syntax for the ``upload`` subcommand:

.. code-block:: console

    $ pymeilisearch upload --template <template> --index <index> <source> <location> [options]

As you can see, this command requires certain arguments and supports additional options, depending
on your requirements.

.. _meilisearch-docs-scrapper: https://github.com/meilisearch/docs-scraper#set-your-config-file

- ``--index <index name>``: Name of the Meilisearch index to use to identify the content.
- ``<source>``: Format type for the documents to upload. It can be ``html``, ``url``, or ``github``.
- ``<location>``: Location of the documents or website to upload.


**Options**

- ``--cname <cname>``: CNAME that hosts the documents. While supplying a CNAME
  is optional, doing so is recommended for localhost scraping.
- ``--port <port>``: Port the localhost is connected on. The default is ``8000``.
- ``--orgs <orgs>``: One or more names of the GitHub organizations to scrape public
  GitHub pages from.


Get the PyMeilisearch version
=============================

The ``version`` command gets the version of your PyMeilisearch`` installation:

.. code-block:: console

    $ pymeilisearch version
