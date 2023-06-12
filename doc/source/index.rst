pymeilisearch documentation |version|
#####################################

Welcome to the official documentation of ``pymeilisearch``.

This project provides a simple command line interface (CLI) to create new
indices in a `meilisearch <https://www.meilisearch.com/>`_ service.

Although `meilisearch provides a Python API
<https://github.com/meilisearch/meilisearch-python>`_, its capabilities are very
limited. As opposite to this API, pymeilisearch offers the following features:

- Pre-defined templates for popular documentation themes
- Documentation scrapping of online websites
- Documentation scrapping of local documentation


.. raw:: html
    :file: _static/search.html

|
|

.. grid:: 2

    .. grid-item-card:: Getting started :fa:`person-running`
        :link: getting-started/index
        :link-type: doc

        Step by step guidelines on how to set up your environment.

    .. grid-item-card:: User guide :fa:`book-open-reader`
        :link: user-guide/index
        :link-type: doc

        Learn about the capabilities, features, and key topics of the project.

    .. grid-item-card:: Contributing :fa:`gavel`
        :link: contributing
        :link-type: doc

        Learn about the capabilities, features, and key topics of the project.

.. jinja:: main_toctree

    {% if build_api or build_examples %}
    .. grid:: 2

       {% if build_api %}
       .. grid-item-card:: API reference :fa:`book-bookmark`
           :link: autoapi/index
           :link-type: doc

           A detailed guide describing the pymeilisearch API. This guide documents all the
           methods and properties for each one of the interfaces, classes and
           enumerations of each one of the modules in pymeilisearch.
        {% endif %}

       {% if build_examples %}
       .. grid-item-card:: Gallery of examples :fa:`laptop-code`
           :link: examples
           :link-type: doc

           Learn how to use pymeilisearch for creating your own indices with
           custom templates from an online website or local HTML files.
        {% endif %}
    {% endif %}


.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting-started/index
       user-guide/index
       {% if build_examples %}
       examples
       {% endif %}
       {% if build_api %}
       autoapi/index
       {% endif %}
       contributing.rst
