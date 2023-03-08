"""
Create an index for each public github page for each repo in orgs using sphinx.
"""
import os

from get_pages import public_gh_pages
from scrape_url import Scraper

from ansys.tools.meilisearch.template_utils import is_sphinx


def scrape_gh_pages_sphinx_docs(orgs):
    """Create an index for each public github page for each repo in orgs.

    The created ``index_uid`` will match ``<repo>-sphinx-docs`` with a ``'-'``
    instead of a ``'/'`` within the repository name. For example:

    The repository ``pyansys/pymapdl`` will be ``pyansys-pymapdl-sphinx-docs``.

    Index UID will also be lowercased

    Parameters
    ----------
    orgs : list[str]
        Organizations to scrape public pages for.

    Notes
    -----
    Requires ``GH_PUBLIC_TOKEN`` to be a GitHub token with public access.

    """

    # first, get all public gh_pages
    token = os.environ.get("GH_PUBLIC_TOKEN")

    urls = {}
    for org in orgs:
        print(f"\n\nQuerying for organization {org}")
        org_urls = public_gh_pages(org, token=token, ignore_githubio=True)
        urls.update(org_urls)

        print("Public URLs with custom CNAMEs")
        for k, v in org_urls.items():
            print(f"{k:40} {v}")

    # for each URL, get those using sphinx
    sphinx_urls = {repo: url for repo, url in urls.items() if is_sphinx(url)}

    print("\n\nURLs using Sphinx")
    for repo, url in sphinx_urls.items():
        print(f"{repo:40} {url}")

    # now, scrape each one individually to create isolated indexes
    for repo, url in sphinx_urls.items():
        repo = repo.replace("/", "-").lower()
        index_uid = f"{repo}-sphinx-docs"
        Scraper.scrape_url(url, index_uid, template="sphinx")


if __name__ == "__main__":
    orgs = ["pyansys", "ansys"]
    scrape_gh_pages_sphinx_docs(orgs)
