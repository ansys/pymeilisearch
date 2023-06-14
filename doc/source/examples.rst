Examples
========



Using pymeilisearch CLI utility
-------------------------------

Creating an index from an online page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an index from an online page, you can use the `pymeilisearch` CLI utility as follows:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> url https://example.com

Creating an index from a local page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an index from a local page, run the following command:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> html /path/to/files

Creating an index from GitHub organizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create indexes for pages of repositories in a GitHub organization, run the
following command:

.. code-block:: shell

   pymeilisearch upload --template <template name or path> --index <index name> github /path/to/files --orgs orgA --orgs orgB

Creating an index from CI/CD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create an index from CI/CD, you can use the `pymeilisearch` CLI utility
within your `Ansys Actions <https://actions.docs.ansys.com>`_ workflow. Here's
an example:

.. tab-set::

    .. tab-item:: Online content

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> url https://example.com

    .. tab-item:: Local content

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> html /path/to/files

    .. tab-item:: GitHub organization

        .. code-block:: yaml

           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name or path> --index <index name> github /path/to/files --orgs orgA --orgs orgB
