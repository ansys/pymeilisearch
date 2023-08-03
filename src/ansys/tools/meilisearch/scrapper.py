"""Module for scaping web pages."""
import os
import subprocess
import tempfile

import requests

from ansys.tools.meilisearch.client import BaseClient
from ansys.tools.meilisearch.templates import render_template
from ansys.tools.meilisearch.templates.utils import get_template


def get_temp_file_name(ext=".txt"):
    """Get the name of the temporary file, which has a ``.txt`` extension."""
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name
    temp_file.close()
    return temp_file_name + ext


class WebScraper(BaseClient):
    """
    Provides for scraping web pages and checking if responses are successful.
    """

    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        """
        Parameters
        ----------
        meilisearch_host_url : str or None, default: None
            URL of the Meilisearch host.
        meilisearch_api_key : str or None, default: None
            API key (admin) of the Meilisearch host.
        """

        super().__init__(meilisearch_host_url, meilisearch_api_key)

    def _load_and_render_template(self, url, template, index_uid, stop_urls=None):
        """Load and render a template file for a URL and unique name.

        Parameters
        ----------
        url : str
            URL for the web page to scrape.
        template : str
            Template file for rendering.
        index_uid : str
            Unique name of the Meilisearch index.
        stop_urls : str or list[str], default: None
            A list of stop points when scraping URLs. If specified, crawling
            will stop when encountering any URL containing any of the strings
            in this list.

        Returns
        -------
        str
            Name of the temporary configuration file that was created.
        """
        temp_config_file = get_temp_file_name(".json")
        render_template(
            template, url, temp_config_file, index_uid=index_uid, stop_urls_default=stop_urls
        )
        return temp_config_file

    def _scrape_url_command(self, temp_config_file):
        """
        Scrape the URL for a web page.

        Parameters
        ----------
        temp_config_file : str
            URL for the web page.

        Returns
        -------
        str
            Output of scraping the URL for the web page.
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
            Output of scraping the URL for the web page.

        Returns
        -------
        int
            Number of hits from the URL.
        """
        if output:
            try:
                n_hits = int(output.strip().splitlines()[-1].split()[-1])
            except ValueError:
                n_hits = 0
        else:
            n_hits = 0
        return n_hits

    def _check_url(self, urls):
        """
        Check if the URL for a web page is valid and accessible.

        Parameters
        ----------
        url : str
            URL for the web page.

        Raises
        ------
        ValueError
            If the URL does not start with ``https://`` or ``http://``.
        RuntimeError
            If the URL returns a non-200 status code.
        """
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            if not url.startswith(("https://", "http://")):
                raise ValueError(
                    f'URLs must start with "https://" or "http://". Instead, "{url}" was returned.'
                )
            response = requests.get(url)
            if response.status_code != 200:
                raise RuntimeError(f'URL "{url}" returned status code {response.status_code}')

    def scrape_url(self, url, index_uid, template=None, stop_urls=None, verbose=False):
        """Scrape a URL for a web page using the active Meilisearch host.

        This method generates a single unique name for a single URL.

        Parameters
        ----------
        url : str
            URL for the web page to scrape.
        index_uid : str
            Unique name of the MeiliSearch index.
        template : str, default: None
            Template file for rendering.
        verbose : bool, default: False
            Whether to print the output from scraping the URL.

        Returns
        -------
        int
            Number of hits from the URL for the web page.
        """
        self._check_url(url)
        template = get_template(url) if template is None else template

        temp_config_file = self._load_and_render_template(url, template, index_uid, stop_urls)
        output = self._scrape_url_command(temp_config_file)

        n_hits = self._parse_output(output)
        if verbose:
            print(output)
        return n_hits

    def scrape_from_directory(self, path, template=None, verbose=False):
        """Scrape the URLs for all web pages in a directory using the active Meilisearch host.

        This method generates a unique index identifier for each URL in the directory.

        Parameters
        ----------
        path : str
            Path to the directory containing the URLs to scrape.
        verbose : bool, default: False
            Whether to print the output of scraping the URLs.

        Returns
        -------
        dict
            Dictionary where keys are unique IDs of indexes and values are the
            number of hits for each URL.

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
