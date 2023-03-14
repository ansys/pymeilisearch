import os
from unittest.mock import Mock, patch

from meilisearch import Client
import pytest

from ansys.tools.meilisearch.client import MeilisearchClient


@pytest.fixture
def meilisearch_client():
    return MeilisearchClient(
        meilisearch_host_url="http://localhost:7700", meilisearch_api_key="masterKey"
    )


def test_constructor_with_env_vars():
    os.environ["MEILISEARCH_HOST_URL"] = "http://localhost:7700"
    os.environ["MEILISEARCH_API_KEY"] = "masterKey"

    client = MeilisearchClient()
    assert client._meilisearch_host_url == "http://localhost:7700"
    assert client._meilisearch_api_key == "masterKey"


def test_constructor_without_env_vars():
    with pytest.raises(RuntimeError):
        MeilisearchClient()


def test_query_index_documents(meilisearch_client):
    client = meilisearch_client
    index_uid = "movies"

    mock_index = Mock()
    mock_index.get_stats.return_value = {"number_of_documents": 100}
    client._client.index.return_value = mock_index

    result = client.query_index_documents(index_uid)
    assert result == 100


def test_fetch_documents(meilisearch_client):
    client = meilisearch_client

    with patch.object(Client, "index") as mock_index:
        mock_index.return_value.documents.return_value = {
            "results": [{"id": 1, "title": "movie1"}, {"id": 2, "title": "movie2"}],
            "total": 2,
        }
        result = client._fetch_documents("movies")

    assert len(result) == 2
    assert result[0]["title"] == "movie1"
    assert result[1]["title"] == "movie2"
