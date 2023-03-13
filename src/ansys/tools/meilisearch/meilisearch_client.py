"""Provide the ``MeilisearchClient`` class"""
import os
from typing import List

from meilisearch import Client
import requests


class MeilisearchClient:
    """
    A base scraper class for scraping web pages and indexing the results in MeiliSearch.

    If no values are passed for `meilisearch_host_url` or `meilisearch_api_key`,
    the constructor will check for their values in environment variables.

    Parameters
    ----------
    meilisearch_host_url : str, default : None
        The URL to the MeiliSearch host.
    meilisearch_api_key : str, default : None
        The admin API key to the MeiliSearch host.

    Raises
    ------
    RuntimeError
        If the `MEILISEARCH_HOST_URL` or `MEILISEARCH_API_KEY`
        environment variables are not set and no values are passed to the constructor.

    """

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Initialize a new instance of the MeilisearchClient class.
        """
        self._meilisearch_host_url = meilisearch_host_url
        self._meilisearch_api_key = meilisearch_api_key

        if self._meilisearch_host_url is None:
            if "MEILISEARCH_HOST_URL" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_HOST_URL is required as the environment variable "MEILISEARCH_HOST_URL"'  # noqa: E501
                )
            self._meilisearch_host_url = os.environ["MEILISEARCH_HOST_URL"]

        if self._meilisearch_api_key is None:
            if "MEILISEARCH_API_KEY" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_API_KEY is required as the environment variable "MEILISEARCH_API_KEY"'  # noqa: E501
                )
            self._meilisearch_api_key = os.environ["MEILISEARCH_API_KEY"]

        self._client = Client(self._meilisearch_host_url, self._meilisearch_api_key)
        self._index_uid = None
        self._index = None
        self.headers = {"Authorization": f"Bearer {self._meilisearch_api_key}"}

    def _delete_index(self):
        """Delete the current MeiliSearch index."""
        self._index.delete()

    def query_index_documents(self, index_uid, delete=False):
        """Query the specified MeiliSearch index for its statistics.

        Parameters
        ----------
        index_uid : str
            The uid of meilisearch to query.

        Returns
        -------
        int
            The number of documents in the MeiliSearch index."""
        self._index_uid = index_uid.replace("/", "-")
        self._index = self._client.index(index_uid)
        if delete:
            self._delete_index()
        stats = self._index.get_stats()
        return stats.number_of_documents

    def _fetch_documents(self, source_index_uid: str, limit: int = 20) -> List[dict]:
        """
        Fetch all documents from the source index and return them as a list.
        """
        offset = 0
        documents = []
        while True:
            # Construct the API URL with the current offset and limit values
            source_index_url = f"{self._meilisearch_host_url}/indexes/{source_index_uid}/documents?limit={limit}&offset={offset}"  # noqa: E501

            # Call the API to fetch the documents
            response = requests.get(source_index_url, headers=self.headers)
            response_json = response.json()
            documents += response_json["results"]

            # Check if all the documents have been fetched
            if offset + limit >= response_json["total"]:
                break

            # Update the offset value for the next iteration
            offset += limit

        return documents
