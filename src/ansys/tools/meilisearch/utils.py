from typing import List

import requests

from .client import MeilisearchClient


class MeilisearchUtils:
    """
    A collection of utility functions for working with MeiliSearch.
    """

    def __init__(self, meilisearch_client: MeilisearchClient):
        self._api = meilisearch_client
        self._headers = {"Authorization": f"Bearer {self._api._meilisearch_api_key}"}

    def fetch_all_documents(self, source_index_uid: str, limit: int = 20) -> List[dict]:
        """
        Fetch all documents from the source index and return them as a list.
        """
        offset = 0
        documents = []
        while True:
            # Construct the API URL with the current offset and limit values
            source_index_url = f"{self._api._meilisearch_host_url}/indexes/{source_index_uid}/documents?limit={limit}&offset={offset}"  # noqa: E501

            # Call the API to fetch the documents
            response = requests.get(source_index_url, headers=self._headers)
            response_json = response.json()
            documents += response_json["results"]

            # Check if all the documents have been fetched
            if offset + limit >= response_json["total"]:
                break

            # Update the offset value for the next iteration
            offset += limit

        return documents
