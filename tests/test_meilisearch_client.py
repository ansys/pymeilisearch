from meilisearch.errors import MeiliSearchApiError
import pytest


def test_query_index_documents(meilisearch_client):
    # create index and add documents
    index_uid = "test_index"
    meilisearch_client.client.create_index(index_uid, {"primaryKey": "id"})
    documents = [{"id": 1, "title": "Test document 1"}, {"id": 2, "title": "Test document 2"}]
    meilisearch_client.client.index(index_uid).add_documents(documents)

    # query index and check result
    num_documents = meilisearch_client.query_index_documents(index_uid)
    assert num_documents == 2

    # delete index and check result
    meilisearch_client._delete_index()
    with pytest.raises(MeiliSearchApiError):
        meilisearch_client.query_index_documents(index_uid)
