"""Module contains ``MeilisearchClient`` class for the scrapper"""
import os

from meilisearch import Client


class BaseClient:
    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Base class for client module.

        Parameters
        ----------
        meilisearch_host_url : str, optional
            Meilisearch host URL, by default None
        meilisearch_api_key : str, optional
            Meilisearch API key, by default None

        Raises
        ------
        RuntimeError
            If `meilisearch_host_url` or `meilisearch_api_key` is None and the corresponding
            environment variable is not set
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

    @property
    def meilisearch_api_key(self):
        return self._meilisearch_api_key

    @property
    def meilisearch_host_url(self):
        return self._meilisearch_host_url


class MeilisearchClient(BaseClient):
    """
    A ``Client`` class for scraping web pages and indexing the results in MeiliSearch.

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
        super().__init__(meilisearch_host_url, meilisearch_api_key)
        self._client = Client(self.meilisearch_host_url, self.meilisearch_api_key)
        self._index_uid = None
        self.headers = {"Authorization": f"Bearer {self.meilisearch_api_key}"}

    @property
    def client(self):
        return self._client
