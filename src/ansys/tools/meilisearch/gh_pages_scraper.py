"""
Create an index for each public github page for each repo in orgs using sphinx.
"""
import os

from ansys.tools.meilisearch.get_pages import GitHubPages
from ansys.tools.meilisearch.meilisearch_scraper import WebScraper
from ansys.tools.meilisearch.template_utils import is_sphinx


def get_public_urls(orgs):
    """Get all public gh_pages for each repo in orgs.

    Returns
    -------
    dict
        A dictionary where keys are repo names and values are URLs to their
        public GitHub pages.

    """
    token = os.environ.get("GH_PUBLIC_TOKEN")
    urls = {}
    for org in orgs:
        print(f"\n\nQuerying for organization {org}")
        github_pages = GitHubPages(org, token=token, ignore_githubio=True)
        org_urls = github_pages.get_public_pages()
        urls.update(org_urls)

        print("Public URLs with custom CNAMEs")
        for k, v in org_urls.items():
            print(f"{k:40} {v}")

    return urls


def get_sphinx_urls(urls):
    """Filter URLs that use Sphinx.

    Parameters
    ----------
    urls : dict
        A dictionary where keys are repo names and values are URLs to their
        public GitHub pages.

    Returns
    -------
    dict
        A dictionary where keys are repo names that use Sphinx and values are
        their URLs.

    """
    sphinx_urls = {repo: url for repo, url in urls.items() if is_sphinx(url)}

    print("\n\nURLs using Sphinx")
    for repo, url in sphinx_urls.items():
        print(f"{repo:40} {url}")

    return sphinx_urls


def create_sphinx_indexes(sphinx_urls, meilisearch_host_url=None, meilisearch_api_key=None):
    """Create an index for each public GitHub page that uses Sphinx.

    The created ``index_uid`` will match ``<repo>-sphinx-docs`` with a ``'-'``
    instead of a ``'/'`` within the repository name. For example:

    The repository ``pyansys/pymapdl`` will be ``pyansys-pymapdl-sphinx-docs``.

    Index UID will also be lowercased.

    Parameters
    ----------
    sphinx_urls : dict
        A dictionary where keys are repo names that use Sphinx and values are
        their URLs.

    Notes
    -----
    Requires ``GH_PUBLIC_TOKEN`` to be a GitHub token with public access.

    """
    for repo, url in sphinx_urls.items():
        repo = repo.replace("/", "-").lower()
        index_uid = f"{repo}-sphinx-docs"
        web_scraper = WebScraper(meilisearch_host_url, meilisearch_api_key)
        web_scraper.scrape_url(url, index_uid, template="sphinx")
