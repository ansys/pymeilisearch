import os

from meilisearch import Client


class MeilisearchClient:
    """
    A base scraper class for scraping web pages and indexing the results in MeiliSearch.

    Parameters
    ----------
    meilisearch_host_url : str
        The URL to the MeiliSearch host.
    meilisearch_api_key : str
        The admin API key to the MeiliSearch host.

    """

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Initialize a new instance of the Scraper class.

        If no values are passed for `meilisearch_host_url` or `meilisearch_api_key`,
        the constructor will check for their values in environment variables.

        Raises
        ------
        RuntimeError
            If the `MEILISEARCH_HOST_URL` or `MEILISEARCH_API_KEY`
            environment variables are not set and no values are passed to the constructor.

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
