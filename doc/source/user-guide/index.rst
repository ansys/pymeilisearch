User guide
==========

Meilisearch stores data in the form of discrete records called *documents*.
It then groups these documents into collections called *indexes*. In an
index's settings, you can customize the search behavior for that index.
The settings for one index do not impact other indexes.

You use PyMeilisearch to scrape and upload files or a website to Meilisearch.
This section describes how to use this command-line interface (CLI) tool
to do the scraping and uploading. It then describes how to integrate Meilisearch into
a website as a web component (search bar).

.. grid:: 2

    .. grid-item-card:: Use PyMeilisearch to scrape and upload :fas:`fa fa-terminal`
        :link: cli-usage
        :link-type: doc

        Learn how to use PyMeilisearch from the command line. Covers the installation
        process and examples of common commands and their usage.

    .. grid-item-card:: Integrate Meilisearch into a website :fas:`fa fa-server`
        :link: web-component
        :link-type: doc

        Integrate Meilisearch in a website by creating a search bar
        component and linking it to a running meilisearch instance.

.. toctree::
   :hidden:
   :maxdepth: 3

   cli-usage
   web-component
