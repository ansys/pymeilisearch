import os
import re
import subprocess
import tempfile

from render_template import render_template
import requests


def get_temp_file_name(ext=".txt"):
    """Return a temporary file name."""
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name
    temp_file.close()
    return temp_file_name + ext


def get_redirected_url(html):
    """Return the redirected URL."""
    match = re.search(r'<meta http-equiv="refresh" content="0; URL=(.*?)">', html)
    if match:
        redirected_url = match.group(1)
        return redirected_url
    else:
        return None


def is_sphinx(url):
    """Determine if a page was built using sphinx."""
    response = requests.get(url)
    html = response.text
    if "Redirecting" in html:
        return is_sphinx(get_redirected_url(html))
    return "sphinx" in html


def get_template(url):
    if is_sphinx(url):
        template = "sphinx"
    else:
        template = "default"
    return template


def scrape_url(url, index_uid, template=None, verbose=False):
    """For a single given URL, scrape it using the active meilisearch host.

    This will generate a single index_uid for a single url.

    This requires both the ``MEILISEARCH_HOST_URL`` and the
    MEILISEARCH_API_KEY`` to be setup.

    Returns
    -------
    int
        Number of hits from url.

    """
    if not url.startswith("https://"):
        raise ValueError(
            "\n\nURLs are expected to start with https://" f'\n\n    Instead, got "{url}"'
        )

    if "MEILISEARCH_HOST_URL" not in os.environ:
        raise RuntimeError(
            "\n\nMEILISEARCH_HOST_URL is required:"
            'as the environment variable "MEILISEARCH_HOST_URL"'
        )

    if "MEILISEARCH_API_KEY" not in os.environ:
        raise RuntimeError(
            "\n\nMEILISEARCH_API_KEY is required "
            'as the environment variable "MEILISEARCH_API_KEY"'
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
    result = subprocess.run(["python", "-m", "scraper", temp_config_file], stdout=subprocess.PIPE)
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape a single URL.")
    parser.add_argument("url", type=str, help="The url to scrape")

    parser.add_argument("index_uid", type=str, help="Unique index.")

    parser.add_argument(
        "--meilisearch-host-url",
        type=str,
        required=False,
        help="The URL to the meilisearch host",
    )

    parser.add_argument(
        "--meilisearch-api-key",
        type=str,
        required=False,
        help="The admin API to the meilisearch host",
    )

    parser.add_argument(
        "--fix_index_uid",
        required=False,
        action="store_true",
        help="Remove any '/' from the index_uid",
    )

    args = parser.parse_args()

    if args.meilisearch_host_url is not None:
        os.environ["MEILISEARCH_HOST_URL"] = args.meilisearch_host_url
    if args.meilisearch_api_key is not None:
        os.environ["MEILISEARCH_API_KEY"] = args.meilisearch_api_key

    if "/" in args.index_uid:
        if args.fix_index_uid:
            index_uid = args.index_uid.replace("/", "-")
        else:
            raise ValueError(
                '`index_uid` cannot contain "/". Either remove it or allow it to '
                "be removed with --fix_index_uid"
            )
    else:
        index_uid = args.index_uid

    print("Scrapping:")
    print(f"URL:       {args.url}")
    print(f"Index UID: {index_uid}")
    n_hits = scrape_url(args.url, index_uid, verbose=True)
