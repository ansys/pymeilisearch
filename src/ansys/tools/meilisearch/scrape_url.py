import os
import subprocess
import tempfile

from render_template import render_template
import requests

from ansys.tools.meilisearch.template_utils import get_template


def get_temp_file_name(ext=".txt"):
    """Return a temporary file name."""
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name
    temp_file.close()
    return temp_file_name + ext


class BaseScraper:
    def __init__(self, meilisearch_host_url=None, meilisearch_api_key=None):
        self.meilisearch_host_url = meilisearch_host_url
        self.meilisearch_api_key = meilisearch_api_key

        if self.meilisearch_host_url is None:
            if "MEILISEARCH_HOST_URL" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_HOST_URL is required as the environment variable "MEILISEARCH_HOST_URL"'  # noqa: E501
                )
            self.meilisearch_host_url = os.environ["MEILISEARCH_HOST_URL"]

        if self.meilisearch_api_key is None:
            if "MEILISEARCH_API_KEY" not in os.environ:
                raise RuntimeError(
                    'MEILISEARCH_API_KEY is required as the environment variable "MEILISEARCH_API_KEY"'  # noqa: E501
                )
            self.meilisearch_api_key = os.environ["MEILISEARCH_API_KEY"]


class Scraper(BaseScraper):
    def scrape_url(self, url, index_uid, template=None, verbose=False):
        """For a single given URL, scrape it using the active Meilisearch host.

        This will generate a single index_uid for a single url.

        Returns
        -------
        int
            Number of hits from url.

        """
        if not url.startswith("https://"):
            raise ValueError(
                "\n\nURLs are expected to start with https://" f'\n\n    Instead, got "{url}"'
            )

        # check URL exists
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f'Url "{url}" returned status code {response.status_code}')

        template = get_template(url) if template is None else template

        # load and render the template
        temp_config_file = get_temp_file_name(".json")
        render_template(template, url, temp_config_file, index_uid=index_uid)

        # Scrape it!
        #
        # this must be run as a system command as twisted will complain:
        # twisted.internet.error.ReactorNotRestartable
        #
        # Plus, it generates a ton of output.
        result = subprocess.run(
            ["python", "-m", "scraper", temp_config_file], stdout=subprocess.PIPE
        )
        output = result.stdout.decode("utf-8")
        if output:
            try:
                n_hits = int(output.strip().splitlines()[-1].split()[-1])
            except ValueError:
                n_hits = 0
        else:
            n_hits = 0

        if verbose:
            print(output)

        return n_hits
