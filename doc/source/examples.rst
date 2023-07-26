Examples
========
This section provides examples that show how to use PyMeilisearch to
create your own indexes with custom templates from online files, local
files, or files in the repositories of GitHub organizations. The final
example shows how you can even use Ansys actions to create one or more
indexes from online files, local files, and files in GitHub organizations.

.. note::
   PyMeilisearch commands require certain arguments and support additional
   options. The commands in the following examples show the general syntax for
   the ``pymeilisearch upload`` command. For information on required arguments
   and supported options for the ``upload`` subcommand, see :ref:`cli-usage`.

Create an index from online files
---------------------------------

This command creates an index from online files:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> url https://example.com

Create an index from local files
--------------------------------

This command creates an index from local files:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> --cname <cname of the document> html /path/to/files

Create indexes from files in GitHub organizations
-------------------------------------------------

This command create indexes from files in the repositories of GitHub organizations:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> github /path/to/files --orgs orgA --orgs orgB

Create an index from CI/CD
--------------------------

You can use PyMeilisearch within `Ansys actions <https://actions.docs.ansys.com>`_ in your CI/CD.
The following tabs show how to use Ansys actions to create one or more indexes from online files,
local files, and files in GitHub organizations:

.. tab-set::

    .. tab-item:: Online files

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> url https://example.com

    .. tab-item:: Local files

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> <cname of the document> html /path/to/files

    .. tab-item:: Files in GitHub organizations

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> github /path/to/files --orgs orgA --orgs orgB
