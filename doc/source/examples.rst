Examples
########

Using pymeilisearch CLI utility
===============================

**Creating an index from an online page**

To create an index from an online page, you can use the `pymeilisearch` CLI utility as follows:

.. code-block:: shell

   pymeilisearch upload --template <template name> --index <index name> url https://example.com

**Creating an index from a local page**

To create an index from a local page, run the following command:

.. code-block:: shell

   pymeilisearch upload --template <template name> --index <index name> html /path/to/files

**Creating an index from GitHub organizations**

To create indexes for pages of repositories in a GitHub organizations, run the following command:

.. code-block:: shell

   pymeilisearch upload --template <template name> --index <index name> github /path/to/files --orgs ansys --orgs pyansys

**Creating an index from CI/CD**

To create an index from CI/CD, you can use the `pymeilisearch` CLI utility within your Ansys Actions workflow. Here's an example:

.. tab-set::

    .. tab-item:: online page

        .. code-block:: yaml
        
           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name> --index <index name> url https://example.com

    .. tab-item:: local page

        .. code-block:: yaml
        
           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name> --index <index name> html /path/to/files

    .. tab-item:: GitHub organizations

        .. code-block:: yaml
        
           - name: Upload to MeiliSearch
             run: |
               pymeilisearch upload --template <template name> --index <index name> github /path/to/files --orgs ansys --orgs pyansys
