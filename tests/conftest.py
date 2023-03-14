import pytest

from ansys.tools.meilisearch.client import MeilisearchClient


@pytest.fixture(scope="session")
def meilisearch_client():
    return MeilisearchClient(
        meilisearch_host_url="http://localhost:7700", meilisearch_api_key="masterKey"
    )
