""""Module containing ``DocsAllPublic`` Class to index all public documents in Meilisearch."""
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
        self.documents_utils = MeilisearchUtils(self._api)

    @property
    def destination_index_uid(self):
        """Return destination index uid."""
        return self._destination_index_uid

    def create_index(self, source_index_uid: str, index_uid: str = None) -> None:
        """
        Create an index with the same primary key as the source index.

        Parameters
        ----------
        source_index_uid : str
            Source index UID.
        index_uid : str, default: None
            The destination index name
        """

        if index_uid is None:
            index_uid = self._temp_destination_index_uid
        source_index = self._api.client.get_index(source_index_uid)
        pkey = source_index.get_primary_key()
        response = self._api.client.create_index(index_uid, {"primaryKey": pkey})
        self.documents_utils._wait_task(response.task_uid)

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
        documents = self.documents_utils.fetch_all_documents(source_index_uid)
        destination_index_url = (
            f"{self._api.meilisearch_host_url}/indexes/{self._temp_destination_index_uid}/documents"
        )
        response = requests.post(destination_index_url, json=documents, headers=self._api.headers)
        self.documents_utils._wait_task(response.json()["taskUid"])

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
        self.create_index(index_uids[0])
        for index_uid in index_uids:
            if index_uid == self._destination_index_uid:
                continue
            self.add_documents_to_temp_index(index_uid)

        # If there is no destination index, create one.
        if self.destination_index_uid not in index_uids:
            self.create_index(index_uids[0], self.destination_index_uid)

        # Swap the temp index with dest index
        self._api.client.swap_indexes(
            [{"indexes": [self._temp_destination_index_uid, self._destination_index_uid]}]
        )
        # Delete the dest index
        self._api.client.index(self._temp_destination_index_uid).delete()
