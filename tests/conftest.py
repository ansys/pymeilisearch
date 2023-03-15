import pytest

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.scrapper import WebScraper


@pytest.fixture(scope="session")
def meilisearch_client():
    return MeilisearchClient(
        meilisearch_host_url="http://localhost:7700", meilisearch_api_key="masterKey"
    )


@pytest.fixture(scope="function")
def scraper(meilisearch_client):
    return WebScraper(
        meilisearch_client.meilisearch_host_url, meilisearch_client.meilisearch_host_url
    )
