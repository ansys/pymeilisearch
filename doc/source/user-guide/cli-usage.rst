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

As you can see, this command requires certain arguments and supports additional options, depending
on your requirements.

**Required arguments**

- ``--template <template>``: Name of the template or the file path where
  the template is located. Available templates are ``sphinx_pydata`` and ``default``.
  The configuration file for a template identifies which content to scrape.
  For an example of a basic configuration file, see `Set your Config File
  <https://github.com/meilisearch/docs-scraper#set-your-config-file>`_ in the README
  for the Meilisearch ``docs-scraper`` repository.

- ``--index <index name>``: Name of the Meilisearch index to use to identify the content.
- ``<source>``: Type of files to upload to Meilisearch. Options are ``html``, ``url``,
  and ``github``.
- ``<location>``: Directory path for the files or website to upload.

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
