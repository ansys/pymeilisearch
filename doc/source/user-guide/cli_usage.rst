Using pymeilisearch CLI utility
===============================

To use the CLI tool, open your terminal or command prompt and run the `pymeilisearch` command,
followed by the desired sub-command and options.

General Syntax:

.. code-block:: console

    $ pymeilisearch <sub-command> [options] [arguments]

Available commands
------------------

The `pymeilisearch` CLI tool provides the following sub-commands:

1. `upload`: Upload files or a website to Meilisearch.
2. `version`: Display the current version of the CLI tool.

Command: upload
~~~~~~~~~~~~~~~~~

The `upload` sub-command allows you to upload files or a website to Meilisearch.
It supports different sources and options depending on your requirements.

Syntax:

.. code-block:: console

    $ pymeilisearch upload --template <template> --index <index> <source> <location> [options]

Required Arguments:

- `--template <template>`: Name of the template to use.
- `--index <index>`: Name of the Meilisearch index used to identify the content.
- `<source>`: Source type. Must be one of 'html', 'url', or 'github'.
- `<location>`: Location of the files or website to upload.

Options:

- `--cname <cname>`: The CNAME in which the documents are hosted (optional).
- `--port <port>`: The port in which the local host has to connect (default: 8000).
- `--orgs <orgs>`: The GitHub organizations from which public URLs are scraped (optional). Accepts multiple values.

Examples:

- Upload files from a local directory:

  .. code-block:: console

      $ pymeilisearch upload --template my_template --index my-index html /path/to/files

- Upload a website using a URL:

  .. code-block:: console

      $ pymeilisearch upload --template my_template --index my-index url https://example.com

- Upload documentation from GitHub organizations:

  .. code-block:: console

      $ pymeilisearch upload --template my_template --index my-index github /path/to/files --orgs ansys --orgs pyansys

Command: version
~~~~~~~~~~~~~~~~~

The `version` sub-command displays the current version of the `pymeilisearch` CLI tool.

Syntax:

.. code-block:: console

    $ pymeilisearch version

Example:

- Display the current version:

  .. code-block:: console

      $ pymeilisearch version
