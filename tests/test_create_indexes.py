from unittest.mock import patch

import pytest

from ansys.tools.meilisearch.create_indexes import create_sphinx_indexes, get_sphinx_urls
from ansys.tools.meilisearch.scrapper import WebScraper
from ansys.tools.meilisearch.templates.utils import is_sphinx


@pytest.fixture(scope="module")
def orgs():
    return ["pyansys"]


@pytest.fixture(scope="module")
def scraper_mock():
    with patch.object(WebScraper, "scrape_url") as mock_scraper:
        yield mock_scraper


@pytest.fixture(scope="module")
def public_urls():
    return {
        "pyansys/dev-guide ": "https://dev.docs.pyansys.com",
        "pyansys/pyansys": "https://docs.pyansys.com",
        "pyansys/actions": "https://actions.docs.pyansys.com",
        "pyansys/pyseascape": "https://seascape.docs.pyansys.com",
    }


def test_get_sphinx_urls(public_urls):
    assert get_sphinx_urls(public_urls) == public_urls


@pytest.mark.parametrize(
    "url",
    [
        "https://dev.docs.pyansys.com",
        "https://docs.pyansys.com",
        "https://actions.docs.pyansys.com",
        "https://seascape.docs.pyansys.com",
    ],
)
def test_is_sphinx(url):
    assert is_sphinx(url)


def test_create_sphinx_indexes(meilisearch_client, scraper_mock, public_urls):
    scraper_mock.return_value = None
    create_sphinx_indexes(
        public_urls,
        meilisearch_client.meilisearch_host_url,
        meilisearch_client.meilisearch_host_url,
    )
    for repo, url in public_urls.items():
        repo = repo.replace("/", "-").lower()
        index_uid = f"{repo}-sphinx-docs"
        scraper_mock.assert_any_call(url, index_uid, template="sphinx")
