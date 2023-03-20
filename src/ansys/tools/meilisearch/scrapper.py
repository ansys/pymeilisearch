"""Module containing ``WebScraper`` class to scrape web pages."""
import os
import subprocess
import tempfile

import requests

from ansys.tools.meilisearch.client import BaseClient
from ansys.tools.meilisearch.templates import render_template
from ansys.tools.meilisearch.templates.utils import get_template


def get_temp_file_name(ext=".txt"):
    """Return a temporary file name."""
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name
    temp_file.close()
    return temp_file_name + ext


class WebScraper(BaseClient):
    """
    A scraper class to scrape web pages and check if the response is successful or not.
    """

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Parameters
        ----------
        meilisearch_host_url : str or None
            The URL of the MeiliSearch host. Default is None.
        meilisearch_api_key : str or None
            The API key of the MeiliSearch host. Default is None.
        """

        super().__init__(meilisearch_host_url, meilisearch_api_key)

    def _load_and_render_template(self, url, template, index_uid):
        """Load and render a template file with URL and index UID.

        Parameters
        ----------
        url : str
            The URL to scrape.
        template : str
            The template file to use for rendering.
        index_uid : str
            The unique identifier of the MeiliSearch.

        Returns
        -------
        str
            The name of the temporary configuration file that was created.
        """
        temp_config_file = get_temp_file_name(".json")
        render_template(template, url, temp_config_file, index_uid=index_uid)
        return temp_config_file

    def _scrape_url_command(self, temp_config_file):
        """
        Scrape a URL by executing the `scraper`.

        Parameters
        ----------
        temp_config_file : str
            The URL to scrape.

        Returns
        -------
        str
            The output of the `scraper` command.
        """
        result = subprocess.run(
            ["python", "-m", "scraper", temp_config_file], stdout=subprocess.PIPE
        )
        output = result.stdout.decode("utf-8")
        return output

    def _parse_output(self, output):
        """
        Parse the output of the scraper to determine the number of hits.

        Parameters
        ----------
        output : str
            The output of the `scraper` command.

        Returns
        -------
        int
            The number of hits from the URL.
        """
        if output:
            try:
                n_hits = int(output.strip().splitlines()[-1].split()[-1])
            except ValueError:
                n_hits = 0
        else:
            n_hits = 0
        return n_hits

    def _check_url(self, url):
        """
        Check if the URL is valid and accessible.

        Parameters
        ----------
        url : str
            The URL to check.

        Raises
        ------
        ValueError
            If the URL does not start with 'https://'.
        RuntimeError
            If the URL returns a non-200 status code.
        """
        if not url.startswith("https://"):
            raise ValueError(
                "\n\nURLs are expected to start with https://" f'\n\n    Instead, got "{url}"'
            )
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f'Url "{url}" returned status code {response.status_code}')

    def scrape_url(self, url, index_uid, template=None, verbose=False):
        """For a single given URL, scrape it using the active Meilisearch host.

        This will generate a single index_uid for a single url.

        Parameters
        ----------
        url : str
            The URL to scrape.
        index_uid : str
            The unique identifier of the MeiliSearch.
        template : str, default : None
            The template file to use for rendering.
        verbose : bool, default : False
            If True, print the output of the `scraper` command.

        Returns
        -------
        int
            The number of hits from the URL.
        """
        self._check_url(url)
        template = get_template(url) if template is None else template
        temp_config_file = self._load_and_render_template(url, template, index_uid)
        output = self._scrape_url_command(temp_config_file)
        n_hits = self._parse_output(output)
        if verbose:
            print(output)
        return n_hits

    def scrape_from_directory(self, path, template=None, verbose=False):
        """For a given directory of URLs, scrape them all using the active Meilisearch host.

        This will generate an index_uid for each URL in the directory.

        Parameters
        ----------
        path : str
            The path to the directory containing the URLs to scrape.
        verbose : bool, default : False
            If True, print the output of the `scraper` command.

        Returns
        -------
        dict
            Dictionary of index_uid to number of hits for each URL.

        Raises
        ------
        FileNotFoundError
            If the specified path does not exist.

        """
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Invalid directory {path}")

        with open(os.path.join(path, "urls.txt")) as fid:
            urls = fid.readlines()
            urls = [line.strip() for line in urls]

        index_uids = [os.path.basename(url).replace(".", "_") for url in urls]

        temp_config_files = []
        for url, index_uid in zip(urls, index_uids):
            self._check_url(url)
            template = get_template(url) if template is None else template
            temp_config_file = self._load_and_render_template(url, template, index_uid)
            temp_config_files.append(temp_config_file)

        results = {}
        for temp_config_file, index_uid in zip(temp_config_files, index_uids):
            output = self._scrape_url_command(temp_config_file)
            n_hits = self._parse_output(output)
            if verbose:
                print(output)
            results[index_uid] = n_hits

        return results
