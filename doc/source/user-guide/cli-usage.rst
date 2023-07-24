Use PyMeilisearch to scrape and upload
######################################

You use PyMeilisearch to scrape and upload files or a website to Meilisearch.
After starting this command-line interface (CLI) tool, you supply a template
for content scraping, a Meilisearch index for identifying the content, and
the format type and location of the source files.

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


Subcommands
~~~~~~~~~~~

The ``pymeilisearch`` command supports these subcommands:

- ``upload``: Upload files or a website to Meilisearch.
- ``version``: Get the current version of PyMeilisearch.


Upload files or a website
-------------------------

The ``upload`` subcommand uploads files or a website to Meilisearch,
creating indexes on the Meilisearch instance.


Here is the general syntax for the ``upload`` subcommand:

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

**Options**

- ``--cname <cname>``: CNAME in which the documents are hosted. While supplying a CNAME
  is optional, doing so is recommended for localhost scraping.
- ``--port <port>``: Port on which the localhost has connected. The default is ``8000``.
- ``--orgs <orgs>``: Names of the one or more GitHub organizations to scrape public
  GitHub pages from.


Get the PyMeilisearch version
-----------------------------

The ``version`` command gets the current version of the ``pymeilisearch``:

.. code-block:: console

    $ pymeilisearch version
