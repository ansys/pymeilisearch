Search Engine Integration
=========================

The MeiliSearch backend can be easily integrated into any web page using a web component.
Follow the steps below to include the search bar in your webpage:

1. Download the `docs-searchbar.js` package from a content delivery network. You can use the following script tag:

   .. code-block:: html

      <script src="https://cdn.jsdelivr.net/npm/docs-searchbar.js@2.4.1/dist/cdn/docs-searchbar.min.js"></script>

2. Initialize the search bar by calling the `docsSearchBar` function with the desired configuration. Here's an example:

   .. code-block:: html

      <script>
      let theSearchBar = docsSearchBar({
          hostUrl: 'https://backend.search.pyansys.com',
          apiKey: 'd5271738ba1a75af83748f615aca07f8a73fc353186ff04f28925104b6f49614',
          indexUid: 'pyansys-docs-all-public',
          inputSelector: '#q',
          debug: false,
          enhancedSearchInput: false,
          enableDarkMode: 'auto'
      })
      </script>

   - Replace `hostUrl` with the URL where your search engine is hosted.
   - Replace `apiKey` with your public API key.
   - Replace `indexUid` with the desired index UID.
   - Modify other options (`debug`, `enhancedSearchInput`, `enableDarkMode`) as needed.

Minimum Working Example
-----------------------

Here's a minimum working example of the search bar with default CSS styling, using the `pyansys-docs-all-public`
index and the public search engine key:

.. literalinclude:: ../_static/simple.html
   :language: html

Search Bar with Customized Styling
----------------------------------

If you want to use the customized search bar shown in the example, you can use the `search.html` 
file available on GitHub:

.. literalinclude:: ../_static/search.html
   :language: html


Please note that you need to place the search.html file in the _static directory alongside 
the RST file for it to be included correctly.
