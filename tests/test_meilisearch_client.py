from meilisearch import Client

from ansys.tools.meilisearch.client import MeilisearchClient


def test_meilisearch_client_initialization(meilisearch_client):
    """Test MeilisearchClient initialization."""
    assert isinstance(meilisearch_client, MeilisearchClient)
    assert isinstance(meilisearch_client.client, Client)
    assert isinstance(meilisearch_client.meilisearch_api_key, str)
    assert isinstance(meilisearch_client.meilisearch_host_url, str)


def test_meilisearch_client_query_index_documents(meilisearch_client):
    """Test MeilisearchClient query_index_documents method."""
    index_uid = "test_index"
    meilisearch_client.client.create_index(index_uid)
    meilisearch_client.client.index(index_uid).add_documents([{"id": 1, "name": "test"}])
    number_of_documents = meilisearch_client.query_index_documents(index_uid)
    assert number_of_documents == 1
