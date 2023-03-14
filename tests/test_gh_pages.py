from unittest.mock import patch

import pytest

from ansys.tools.meilisearch.create_indexes import (
    create_sphinx_indexes,
    get_public_urls,
    get_sphinx_urls,
)
from ansys.tools.meilisearch.get_pages import GitHubPages
from ansys.tools.meilisearch.scrapper import WebScraper


@pytest.fixture
def mock_github_pages():
    with patch.object(GitHubPages, "__init__", lambda *args, **kwargs: None):
        with patch.object(
            GitHubPages, "get_public_pages", return_value={"repo1": "https://sphinx-docs1.org"}
        ):
            yield GitHubPages


@pytest.fixture
def mock_requests():
    with patch("ansys.tools.meilisearch.scrapper.requests") as mock:
        mock.get.return_value.status_code = 200
        mock.get.return_value.text = "<html><body>test</body></html>"
        yield mock


def test_create_sphinx_indexes(mock_github_pages, mock_requests):
    urls = get_public_urls(["org1"])
    assert urls == {"repo1": "https://sphinx-docs1.org"}

    sphinx_urls = get_sphinx_urls(urls)
    assert sphinx_urls == {"repo1": "https://sphinx-docs1.org"}

    with patch.object(WebScraper, "__init__", lambda *args, **kwargs: None), patch.object(
        WebScraper, "scrape_url"
    ) as mock_scrape_url:
        create_sphinx_indexes(sphinx_urls)
        mock_scrape_url.assert_called_once_with(
            "https://sphinx-docs1.org",
            "repo1-sphinx-docs",
            template="sphinx",
            meilisearch_host_url=None,
            meilisearch_api_key=None,
        )
