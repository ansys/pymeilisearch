:orphan:

API reference
=============

This section describes PyMeilisearch API endpoints, their capabilities,
and how to interact with them programmatically.

.. toctree::
   :titlesonly:
   :maxdepth: 3

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}