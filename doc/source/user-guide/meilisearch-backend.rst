
MeiliSearch backend
###################
Decide whether you want to deploy `Meilisearch`_ using a Docker image or use a cloud service. 
  
* Docker image: MeiliSearch provides an official Docker image that allows you to easily run the search engine as a container. 

* Cloud service: Use a cloud service provider that offers managed MeiliSearch instances.

In both cases, pymeilisearch expects the backend url and key as environment variable as MEILISEARCH_HOST_URL 
and MEILISEARCH_API_KEY respectively.

.. _meilisearch: https://www.meilisearch.com/

Search engine configuration
---------------------------

Create configuration templates to define the structure and settings of your search index.
PyMeilisearch provides configuration templates that you can use to customize the behavior 
and settings of your MeiliSearch instance. These templates include options such as search parameters, 
indexing configurations, and filtering options. By modifying these templates according to your specific needs, 
you can fine-tune the search experience and optimize the indexing process.

PyMeilisearch provide two in-build template `sphinx_pydata` and `default`.

An example for the json file is as shown below:

.. literalinclude:: ../_static/config.json
   :language: json   

Configuring different versions of documentation and ansys sphinx theme
----------------------------------------------------------------------
Documentation versions: PyMeilisearch allows you to scrape and index documentation from various sources, 
including online repositories or local files. You can configure PyMeilisearch to handle multiple versions 
of your documentation, ensuring that users can search and access documentation relevant to the version 
they are using by multiple indexUids. By organizing your documentation into different versions, you can
provide accurate and version-specific search results.

Ansys sphinx theme: Ansys sphinx theme supports PyMeilisearch , allowing you to maintain a consistent and 
visually appealing documentation layout as documented in 
`Ansys sphinx theme documentation`_.
By integrating the theme options with indexUid scraped with pymeilisearch, The search button is able start using meilisearch engine.

.. _Ansys sphinx theme documentation: https://sphinxdocs.ansys.com/version/stable/user_guide/options.html#use-meilisearch

Setting up GitHub actions for automation
----------------------------------------
GitHub Actions: GitHub Actions is a powerful workflow automation tool. You can leverage GitHub Actions to automate 
the process of scraping and indexing your documentation with PyMeilisearch. By creating custom workflows using GitHub Actions, 
you can define triggers, actions, and schedules to keep your MeiliSearch instance updated with the latest changes in your documentation repository.

Configuration: To set up PyMeilisearch with GitHub Actions, create a workflow file (for example, main.workflow) in your repository's 
.github/workflows directory. Define the desired workflow, such as triggering on a push or schedule, and 
specify the actions to be performed, including scraping and indexing the documentation using PyMeilisearch.

Authentication and secrets: Ensure that you store required authentication for the meilisearch 
instance as environment variable of `MEILISEARCH_HOST_URL`and `MEILISEARCH_API_KEY`.