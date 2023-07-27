"""Module providing the Meilisearch client."""
import os

from meilisearch import Client


class BaseClient:
    """Provides the base class for the Meilisearch client."""

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Initialize the Meilisearch client.

        Parameters
        ----------
        meilisearch_host_url : str, default: None
            URL for the Meilisearch host.
        meilisearch_api_key : str, default: None
            API key (admin) for the Meilisearch host.

        Raises
        ------
        RuntimeError
            If the ``meilisearch_host_url`` or ``meilisearch_api_key`` parameter
            is ``None`` and the corresponding environment variable is not set.
        """
        self._meilisearch_host_url = meilisearch_host_url
        self._meilisearch_api_key = meilisearch_api_key

        if self._meilisearch_host_url is None:
            if "MEILISEARCH_HOST_URL" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_HOST_URL is required as the environment variable "MEILISEARCH_HOST_URL".'  # noqa: E501
                )
            self._meilisearch_host_url = os.environ["MEILISEARCH_HOST_URL"]

        if self._meilisearch_api_key is None:
            if "MEILISEARCH_API_KEY" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_API_KEY is required as the environment variable "MEILISEARCH_API_KEY".'  # noqa: E501
                )
            self._meilisearch_api_key = os.environ["MEILISEARCH_API_KEY"]

    @property
    def meilisearch_api_key(self):
        """Meilisearch API key."""
        return self._meilisearch_api_key

    @property
    def meilisearch_host_url(self):
        """Meilisearch host URL."""
        return self._meilisearch_host_url


class MeilisearchClient(BaseClient):
    """
    Provides for scraping documents and indexing content in Meilisearch.

    If no values are passed for the ``meilisearch_host_url`` or ``meilisearch_api_key``
    parameters, the constructor checks for their values in environment variables.

    """

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Initialize a new instance of the ``MeilisearchClient`` class.

        Parameters
        ----------
        meilisearch_host_url : str, default: None
            URL for the Meilisarch host.
        meilisearch_api_key : str, default: None
            API key (admin) for the Meilisearch host.

        Raises
        ------
        RuntimeError
            If the ``MEILISEARCH_HOST_URL`` or ``MEILISEARCH_API_KEY``
            environment variables are not set and no values are passed to the constructor
            for initializing a new instance of the ``MeilisearchClient`` class.
        """
        super().__init__(meilisearch_host_url, meilisearch_api_key)
        self._client = Client(self.meilisearch_host_url, self.meilisearch_api_key)
        self._index_uid = None
        self.headers = {"Authorization": f"Bearer {self.meilisearch_api_key}"}

    @property
    def client(self):
        """Meilisearch client."""
        return self._client
