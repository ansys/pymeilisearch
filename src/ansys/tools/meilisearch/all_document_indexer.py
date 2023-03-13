import json
import time
from typing import List

import requests

from ansys.tools.meilisearch.meilisearch_client import MeilisearchClient


class DocsAllPublic:
    """Class to index all public documents in Meilisearch.

    Parameters
    ----------
    meilisearch_host_url : str
        Meilisearch host URL. Defaults to None.
    meilisearch_api_key : str
        Meilisearch API key. Defaults to None.
    destination_index_uid : str
        Destination index UID. Defaults to "pyansys-docs-all-public".
    """

    def __init__(
        self,
        meilisearch_host_url: str = None,
        meilisearch_api_key: str = None,
        destination_index_uid: str = "pyansys-docs-all-public",
    ):
        self.api = MeilisearchClient(meilisearch_host_url, meilisearch_api_key)
        self.destination_index_uid = destination_index_uid
        self.temp_destination_index_uid = f"temp_{destination_index_uid}"

    def _wait_task(self, task_uid: int, timeout: float = 10.0) -> None:
        """
        Wait until a task is complete.

        If a task exceeds the timeout, raise a TimeoutError.

        parameters
        ----------
        task_uid : int
            Task UID.
        timeout : float
            Timeout value in seconds. Defaults to 10.0.
        """
        task_url = f"{self.api._meilisearch_host_url}/tasks/{task_uid}"
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            response = requests.get(task_url, headers=self.api.headers)
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
            else:
                time.sleep(1)
        if time.time() > timeout_time:
            raise TimeoutError(f"Exceeded timeout {timeout}")

    def create_temp_index(self, source_index_uid: str) -> None:
        """
        Create a temp index with the same primary key as the source index.

        Parameters
        ----------
        source_index_uid : str
            Source index UID.
        """
        source_index = self.api._client.get_index(source_index_uid)
        pkey = source_index.get_primary_key()
        response = self.api._client.create_index(
            self.temp_destination_index_uid, {"primaryKey": pkey}
        )
        self._wait_task(response.task_uid)

    def add_documents_to_temp_index(self, source_index_uid: str) -> None:
        """
        Fetch all the documents from the source index and add them to the temp index.
        """
        # Fetch all the documents from the source index and add them to the
        # temporary destination index
        documents = self.api._fetch_documents(source_index_uid)
        destination_index_url = (
            f"{self.api._meilisearch_host_url}/indexes/{self.destination_index_uid}/documents"
        )
        response = requests.post(destination_index_url, json=documents, headers=self.api.headers)
        self._wait_task(response.json()["taskUid"])

    def add_all_public_doc(self, selected_keys: List[str] = ["ansys, pyansys"]) -> None:
        """
        Add all public documents to the destination index.

        Parameters
        ----------
        selected_keys : List[str], optional
            If specified, only indexes whose keys start with one of the specified
            strings will be included in the search. Defaults to ["ansys, pyansys"]
        """
        stats = self.api._client.get_all_stats()
        index_uids = [
            key for key in stats["indexes"].keys() if key.startswith(tuple(selected_keys))
        ]
        source_index = self.api._client.get_index(index_uids[0])
        self.create_temp_index(source_index)
        for index_uid in index_uids:
            if index_uid == self.destination_index_uid:
                continue
            self.add_documents_to_temp_index(index_uid)

        # Swap the temp index with dest index
        self.api._client.swap_indexes(
            {"indexes": [self.temp_destination_index_uid, self.destination_index_uid]}
        )
        # Delete the dest index
        self.api._client.index(self.temp_destination_index_uid).delete()
