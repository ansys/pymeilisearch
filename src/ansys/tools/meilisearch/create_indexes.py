"""
Create an index for each public GitHub page for each repository in
one or more organizations using Sphinx.
"""
import os

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.get_pages import GitHubPages
from ansys.tools.meilisearch.scrapper import WebScraper
from ansys.tools.meilisearch.templates.utils import is_sphinx
from ansys.tools.meilisearch.utils import MeilisearchUtils


def get_public_urls(orgs):
    """Get all public GitHub pages (gh_pages) for each repository in one or more organizations.

    Parameters
    ----------
    orgs : str or list[str]
        One or more GitHub organizations to get public GitHub pages from.

    Returns
    -------
    dict
        Dictionary where keys are repository names and values are URLs to their
        public GitHub pages.

    """
    token = os.environ.get("GH_PUBLIC_TOKEN")
    urls = {}
    for org in orgs:
        github_pages = GitHubPages(org, token=token, ignore_githubio=True)
        org_urls = github_pages.get_public_pages()
        urls.update(org_urls)
        for key, value in org_urls.items():
            print(f"{key:40} {value}")
    return urls


def get_sphinx_urls(urls):
    """Get URLs for pages that were generated using Sphinx.

    Parameters
    ----------
    urls : dict
        Dictionary where keys are repository names and values are URLs to their
        public GitHub pages.

    Returns
    -------
    dict
        Dictionary where keys are repository names that use Sphinx and
        values are their URLs.

    """
    return {repo: url for repo, url in urls.items() if is_sphinx(url)}


def create_sphinx_indexes(
    sphinx_urls,
    stop_urls=None,
    meilisearch_host_url=None,
    meilisearch_api_key=None,
):
    """Create an index for each public GitHub page that was generated using Sphinx.

    The unique name created for the index (``index_uid``) matches ``<repo>-sphinx-docs``,
    with a ``'-'`` instead of a ``'/'`` in the repository name. For example, the unique
    ID created for the ``pyansys/pymapdl`` repository has ``pyansys-pymapdl-sphinx-docs``
    as its unique name.

    The unique name for an index is always lowercase.

    Parameters
    ----------
    sphinx_urls : dict
        Dictionary where keys are repository names that use Sphinx and values are
        their URLs.
    stop_urls : str or list[str], default: None
        A list of stop points when scraping URLs. If specified, crawling
        will stop when encountering any URL containing any of the strings
        in this list.
    meilisearch_host_url : str, default: None
        URL for the Meilisarch host.
    meilisearch_api_key : str, default: None
        API key (admin) for the Meilisearch host.

    Notes
    -----
    This method requires that the ``GH_PUBLIC_TOKEN`` environment variable
    be a GitHub token with public access.

    """
    for repo, url in sphinx_urls.items():
        repo = repo.replace("/", "-").lower()
        index_uid = f"{repo}-sphinx-docs"
        temp_index_uid = f"temp-{repo}-sphinx-docs"
        web_scraper = WebScraper(meilisearch_host_url, meilisearch_api_key)
        web_scraper.scrape_url(url, temp_index_uid)
        client = MeilisearchClient(meilisearch_host_url, meilisearch_api_key)
        document_utils = MeilisearchUtils(client)
        stats = client.client.get_all_stats()
        index_uids = list(stats["indexes"].keys())
        if not index_uid in index_uids:
            response = client.client.create_index(index_uid, {"primaryKey": "objectID"})
            document_utils._wait_task(response.task_uid)
        swap_response = client.client.swap_indexes([{"indexes": [temp_index_uid, index_uid]}])
        client.client.index(temp_index_uid).delete()


def scrap_web_page(
    index_uid, url, templates, stop_urls=None, meilisearch_host_url=None, meilisearch_api_key=None
):
    """
    Scrape a web page and index its content in Meilisearch.

    Parameters
    ----------
    index_uid : str
        Unique name to give to the Meilisearch index.
    url : str
        URL of the web page to scrape.
    templates : str or list[str]
        One or more templates to use to know what content is to
        be scraped. Available templates are ``sphinx_pydata`` and ``default``.
    stop_urls : str or list[str], default: None
        A list of stop points when scraping URLs. If specified, crawling
        will stop when encountering any URL containing any of the strings
        in this list.
    meilisearch_host_url : str, default: None
        URL for the Meilisarch host.
    meilisearch_api_key : str, default: None
        API key (admin) for the Meilisearch host.
    """
    client = MeilisearchClient(meilisearch_host_url, meilisearch_api_key)
    web_scraper = WebScraper(meilisearch_host_url, meilisearch_api_key)
    web_scraper.scrape_url(url, index_uid, templates, stop_urls)
    document_utils = MeilisearchUtils(client)
    stats = client.client.get_all_stats()
    index_uids = list(stats["indexes"].keys())
    if index_uid not in index_uids:
        response = client.client.create_index(index_uid, {"primaryKey": "objectID"})
        document_utils._wait_task(response["taskUid"])
