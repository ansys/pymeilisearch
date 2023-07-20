PyMeilisearch documentation |version|
#####################################

PyMeilisearch provides a simple command line interface (CLI) to create
indices in a `Meilisearch <https://www.meilisearch.com/>`_ service.

Because the `Meilisearch Python API <https://github.com/meilisearch/meilisearch-python>`_
provides only limited capabilities, PyMeilisearch was designed to provide more
extensive capabilities, including these:

- Predefined templates for popular documentation themes
- Scrapping of documentation on websites
- Scrapping of local documentation


.. raw:: html
    :file: _static/search.html

|
|

.. grid:: 2

    .. grid-item-card:: Getting started :fa:`person-running`
        :link: getting-started/index
        :link-type: doc

        Learn how to install PyMeilisearch and build your own Docker image for
        testing PyMeilisearch locally.

    .. grid-item-card:: User guide :fa:`book-open-reader`
        :link: user-guide/index
        :link-type: doc

        Learn how to use the PyMeilisearch CLI and integrate PyMeilisearch
        in a website.

.. jinja:: main_toctree

    {% if build_api or build_examples %}
    .. grid:: 2

       {% if build_api %}
       .. grid-item-card:: API reference :fa:`book-bookmark`
           :link: autoapi/index
           :link-type: doc

           Learn about PyMeilisearch API endpoints, their capabilities, and
           how to interact with them programmatically.
        {% endif %}

       {% if build_examples %}
       .. grid-item-card:: Examples :fa:`laptop-code`
           :link: examples
           :link-type: doc

           Learn how to use PyMeilisearch to create your own indices with
           custom templates from either an online website or local HTML files.
        {% endif %}
    {% endif %}


.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting-started/index
       user-guide/index
       {% if build_api %}
       autoapi/index
       {% endif %}
       {% if build_examples %}
       examples
       {% endif %}
       contributing.rst
