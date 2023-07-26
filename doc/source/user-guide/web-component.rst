Integrate Meilisearch into a website
####################################

Meilisearch can be integrated into any website as a web component (search bar)
that is linked to a running Meilisearch instance.

Add the search bar to a web page
================================

To add a search bar to a web page, follow these steps:

#. Download the ``docs-searchbar.js`` package from a content delivery network.
   You can use this script tag:

   .. code-block:: html

       <script src="https://cdn.jsdelivr.net/npm/docs-searchbar.js@2.4.1/dist/cdn/docs-searchbar.min.js"></script>

#. Initialize the search bar by calling the ``docsSearchBar`` function with the
   desired configuration. Here is an example:

   .. code-block:: html

       <script>
       let theSearchBar = docsSearchBar({
           hostUrl: 'https://backend.search.pyansys.com',
           apiKey: 'd5271738ba1a75af83748f615aca07f8a73fc353186ff04f28925104b6f49614',
           indexUid: 'ansys-pyansys-sphinx-docs',
           inputSelector: '#q',
           debug: false,
           enhancedSearchInput: false,
           enableDarkMode: 'auto'
       })
       </script>

   - Replace the value shown for the ``hostUrl`` option with the URL where your search
     engine is hosted.
   - Replace the value shown for the ``apiKey`` option  with your public API key.
   - Replace the value shown for the ``indexUid`` option with the unique ID for the
     desired index.
   - Modify values for other options (``debug``, ``enhancedSearchInput``, and
     ``enableDarkMode``) as needed.


This example shows how to add a search bar to a web page and link it
to a Meilisearch instance:

.. literalinclude:: ../_static/simple.html
   :language: html


Customize the style of the search bar
=====================================

Because the search bar is an HTML component, you can use CSS to
customize its style. Here is an example:

.. literalinclude:: ../_static/search.html
   :language: html
