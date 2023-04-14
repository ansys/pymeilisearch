"""Provides the ``MeilisearchUtils`` class module."""
import json
import time
from typing import List

import requests

from ansys.tools.meilisearch.client import MeilisearchClient


class MeiliSearchApiError(Exception):
    pass


class MeiliSearchApiTimeout(Exception):
    pass


class MeilisearchUtils:
    """
    A collection of utility functions for working with MeiliSearch.
    """

    def __init__(self, meilisearch_client: MeilisearchClient):
        """The meilisearch client initilaise.

        Parameters
        ----------
        meilisearch_client : MeilisearchClient
            Meilisearch client."""
        self._api = meilisearch_client
        self._headers = {"Authorization": f"Bearer {self._api._meilisearch_api_key}"}

    def fetch_all_documents(self, source_index_uid: str, limit: int = 20) -> List[dict]:
        """
        Fetch all documents from the source index and return them as a list.

        Parameters
        ----------
        source_index_uid : str
            The index ID of document to fetch.
        limit : int
            The limit of document in single offset.

        Returns
        -------
        document : list
            All the documents fetch from the source document.
        """
        offset = 0
        documents = []
        while True:
            # Construct the API URL with the current offset and limit values
            source_index_url = f"{self._api.meilisearch_host_url}/indexes/{source_index_uid}/documents?limit={limit}&offset={offset}"  # noqa: E501

            # Call the API to fetch the documents
            response = requests.get(source_index_url, headers=self._headers)
            response_json = response.json()

            for document in response_json["results"]:
                document["id"] = document["objectID"]
            documents += response_json["results"]

            # Check if all the documents have been fetched
            if offset + limit >= response_json["total"]:
                break

            # Update the offset value for the next iteration
            offset += limit

        return documents

    def _wait_task(self, task_uid: int, timeout: float = 60.0) -> None:
        """
        Wait until a task is complete.

        If a task exceeds the timeout, raise a MeiliSearchApiTimeout.

        Parameters
        ----------
        task_uid : int
            Task UID.
        timeout : float
            Timeout value in seconds. Defaults to 60.0.

        Raises
        ------
        MeiliSearchApiTimeout
            Raised when the timeout is exceeded.
        RuntimeError
            Raised when the status of the task is failed.
        """
        task_url = f"{self._api.meilisearch_host_url}/tasks/{task_uid}"
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            response = requests.get(task_url, headers=self._headers)
            try:
                jresp = response.json()
            except json.decoder.JSONDecodeError as e:
                raise MeiliSearchApiError(f"Failed to decode response: {e}") from e
            if jresp["status"] == "failed":
                if "error" in jresp:
                    msg = jresp["error"]["message"]
                    raise RuntimeError(f"Task failed:\n\n{msg}")
                else:
                    msg = json.dumps(jresp, indent=2)
                    raise RuntimeError(f"Task failed:\n\n{msg}")
            elif jresp["status"] == "succeeded":
                break
            else:
                time.sleep(1)
        if time.time() > timeout_time:
            raise MeiliSearchApiTimeout(f"Timeout exceeded: {timeout} seconds")
