"""Provides utilities for Meilisearch."""
import json
import time
from typing import List

import requests

from ansys.tools.meilisearch.client import MeilisearchClient


class MeilisearchUtils:
    """
    Provides utility functions for working with Meilisearch.
    """

    def __init__(self, meilisearch_client: MeilisearchClient):
        """Initialize the Meilisearch client.

        Parameters
        ----------
        meilisearch_client : MeilisearchClient
            Meilisearch client."""
        self._api = meilisearch_client
        self._headers = {"Authorization": f"Bearer {self._api._meilisearch_api_key}"}

    def fetch_all_documents(self, source_index_uid: str, limit: int = 20) -> List[dict]:
        """
        Fetch all documents from a source index and return them as a list.

        Parameters
        ----------
        source_index_uid : str
            Unique name of the index to fetch documents from.
        limit : int, default: 20
            The maximum number of documents to fetch in a single offset or query.
            This parameter determines how many documents are included in each response
            when fetching data. The default value is 20.

        Returns
        -------
        list
            List of all documents fetched from the source index.
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

    def _wait_task(self, task_uid: int, timeout: float = 20.0) -> None:
        """
        Wait until a task is complete.

        Parameters
        ----------
        task_uid : int
            Unique name of the task.
        timeout : float, default: 20.0
            Timeout value in seconds for the task. If a task exceeds this
            timeout value, an error is raised.

        Raises
        ------
        TimeoutError
            Raised when the timeout value for the task is exceeded.
        RuntimeError
            Raised when the task fails.
        """
        task_url = f"{self._api.meilisearch_host_url}/tasks/{task_uid}"
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            response = requests.get(task_url, headers=self._api.headers)
            jresp = response.json()
            if jresp["status"] == "failed":
                if "error" in jresp:
                    msg = jresp["error"]["message"]
                    raise RuntimeError(f"Task failed:\n\n{msg}")
                else:
                    msg = json.dumps(jresp, indent=2)
                    raise RuntimeError(f"Task failed:\n\n{msg}")
            elif jresp["status"] == "succeeded":
                break
            elif jresp["status"] == "enqueued":
                break
            else:
                time.sleep(1)
        if time.time() > timeout_time:
            raise TimeoutError(f"Exceeded timeout {timeout}")
