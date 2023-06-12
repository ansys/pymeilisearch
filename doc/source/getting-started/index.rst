Getting started
###############

Getting started with PyMeilisearch is quick and straightforward. This guide will walk you through the initial steps to set up and integrate MeiliSearch into your Python project.

Prerequisites
-------------
Before getting started, ensure that you have the following prerequisites:

* Python: Make sure you have Python installed on your system. PyMeilisearch supports Python 3.6 and above.

* MeiliSearch Backend: Decide whether you want to deploy MeiliSearch using a Docker image or use a cloud service. 
  Docker Image: MeiliSearch provides an official Docker image that allows you to easily run the search engine as a container. 
  You can pull the MeiliSearch image from Docker Hub and run it on your local machine or in a container orchestration
  platform like Kubernetes. Docker provides a standardized and portable environment for running MeiliSearch, 
  making it convenient for local development and deployment.

  Cloud Service: Alternatively, you can use a cloud service provider that offers managed MeiliSearch instances. 
  These services take care of infrastructure setup, scaling, and maintenance, allowing you to focus on 
  integrating MeiliSearch into your application without worrying about the backend infrastructure. 
  Cloud services provide a scalable and reliable solution for hosting MeiliSearch, 
  making it suitable for production environments.

* Configuration Templates: Create configuration templates to define the structure and settings of your search index.
  PyMeilisearch provides configuration templates that you can use to customize the behavior 
  and settings of your MeiliSearch instance. These templates include options such as search parameters, 
  indexing configurations, and filtering options. By modifying these templates according to your specific needs, 
  you can fine-tune the search experience and optimize the indexing process.

Configuring Different Versions of Docs and Ansys Sphinx Theme
-------------------------------------------------------------
Documentation Versions: PyMeilisearch allows you to scrape and index documentation from various sources, 
including online repositories or local files. You can configure PyMeilisearch to handle multiple versions 
of your documentation, ensuring that users can search and access documentation relevant to the version 
they are using by multiple index uids. By organizing your documentation into different versions, you can
provide accurate and version-specific search results.

Ansys Sphinx Theme: Ansys Sphinx theme supports PyMeilisearch , allowing you to maintain a consistent and 
visually appealing documentation layout as documented in 
`Ansys sphinx theme documentation <https://sphinxdocs.ansys.com/version/stable/user_guide/options.html#use-meilisearch>`_.
By integarting the theme options with index-uid scraped with pymeilisearch, The search button will start using meilisearch engine.
