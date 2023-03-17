""""Module containing ``DocsAllPublic`` Class to index all public documents in Meilisearch."""
import json
import time
from typing import List

import requests

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.utils import MeilisearchUtils


class DocsAllPublic:
    """Class to index all public documents in Meilisearch.

    Parameters
    ----------
    meilisearch_client : MeilisearchClient
        Meilisearch client.
    destination_index_uid : str
        Destination index UID. Defaults to "pyansys-docs-all-public".
    """

    def __init__(
        self,
        meilisearch_client: MeilisearchClient,
        destination_index_uid: str = "pyansys-docs-all-public",
    ):
        self._api = meilisearch_client
        self._destination_index_uid = destination_index_uid
        self._temp_destination_index_uid = f"temp-{destination_index_uid}"

    @property
    def destination_index_uid(self):
        """Return destination index uid."""
        return self._destination_index_uid

    def _wait_task(self, task_uid: int, timeout: float = 10.0) -> None:
        """
        Wait until a task is complete.

        If a task exceeds the timeout, raise a TimeoutError.

        Parameters
        ----------
        task_uid : int
            Task UID.
        timeout : float
            Timeout value in seconds. Defaults to 10.0.

        Raises
        ------
        TimeoutError
            Raised when the ``timeout`` is exceed.
        RuntimeError
            Raised when the status of ``task`` failed.
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
            else:
                time.sleep(1)
        if time.time() > timeout_time:
            raise TimeoutError(f"Exceeded timeout {timeout}")

    def create_temp_index(self, source_index_uid: str) -> None:
        """
        Create a temperory index with the same primary key as the source index.

        Parameters
        ----------
        source_index_uid : str
            Source index UID.
        """
        source_index = self._api.client.get_index(source_index_uid)
        pkey = source_index.get_primary_key()
        response = self._api.client.create_index(
            self._temp_destination_index_uid, {"primaryKey": pkey}
        )
        self._wait_task(response["taskUid"])

    def add_documents_to_temp_index(self, source_index_uid: str) -> None:
        """
        Fetch all the documents from the source index and add them to the temp index.

        Parameters
        ----------
        source_index_uid : str
            The index ID of document to fetch.
        """
        # Fetch all the documents from the source index and add them to the
        # temporary destination index
        documents_utils = MeilisearchUtils(self._api)
        documents = documents_utils.fetch_all_documents(source_index_uid)
        destination_index_url = (
            f"{self._api._meilisearch_host_url}/indexes/{self._destination_index_uid}/documents"
        )
        print("adding docs")
        response = requests.post(destination_index_url, json=documents, headers=self._api.headers)
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
        stats = self._api.client.get_all_stats()
        index_uids = [
            key for key in stats["indexes"].keys() if key.startswith(tuple(selected_keys))
        ]
        self.create_temp_index(index_uids[0])
        for index_uid in index_uids:
            if index_uid == self._destination_index_uid:
                continue
            self.add_documents_to_temp_index(index_uid)

        # Swap the temp index with dest index
        self._api.client.swap_indexes(
            {"indexes": [self._temp_destination_index_uid, self._destination_index_uid]}
        )
        # Delete the dest index
        self._api.client.index(self._temp_destination_index_uid).delete()
