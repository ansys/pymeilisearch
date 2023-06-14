Web component
#############

Meilisearch can be integrated into any website as a web component. A search bar
can be created and linked to a running instance of Meilisearch.

Search bar component
====================

Follow the steps below to include a search bar component in a webpage:

#. Download the ``docs-searchbar.js`` package from a content delivery network.
   You can use the following script tag:

   .. code-block:: html

       <script src="https://cdn.jsdelivr.net/npm/docs-searchbar.js@2.4.1/dist/cdn/docs-searchbar.min.js"></script>

#. Initialize the search bar by calling the ``docsSearchBar`` function with the
   desired configuration. Here's an example:

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

   - Replace ``hostUrl`` with the URL where your search engine is hosted.
   - Replace ``apiKey`` with your public API key.
   - Replace ``indexUid`` with the desired index UID.
   - Modify other options (``debug``, ``enhancedSearchInput``, ``enableDarkMode``) as needed.


The following example illustrates how to include a search bar component inside
an html document and link it with a meilisearch backend.

.. literalinclude:: ../_static/simple.html
   :language: html


Customizing the style
=====================

Since the search bar is an html component, it is possible to use CSS to
customize its style.

.. literalinclude:: ../_static/search.html
   :language: html
