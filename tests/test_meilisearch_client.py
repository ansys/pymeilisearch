from meilisearch import Client

from ansys.tools.meilisearch.client import MeilisearchClient


def test_meilisearch_client_initialization(meilisearch_client):
    """Test MeilisearchClient initialization."""
    assert isinstance(meilisearch_client, MeilisearchClient)
    assert isinstance(meilisearch_client.client, Client)
    assert isinstance(meilisearch_client.meilisearch_api_key, str)
    assert isinstance(meilisearch_client.meilisearch_host_url, str)
