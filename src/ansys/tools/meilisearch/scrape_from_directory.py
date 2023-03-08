import os
import subprocess
import tempfile

from render_template import render_template


def get_temp_file_name(ext=".txt"):
    """Return a temporary file name."""
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name
    temp_file.close()
    return temp_file_name + ext


def scrape_from_directory(path, verbose=False):
    """For a single given URL, scrape it using the active meilisearch host.

    This will generate a single index_uid for a single url.

    This requires both the ``MEILISEARCH_HOST_URL`` and the
    MEILISEARCH_API_KEY`` to be setup.

    Returns
    -------
    int
        Number of hits from url.

    """

    if not os.path.isdir(path):
        raise FileNotFoundError(f"Invalid directory {path}")

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

    with open(os.path.join(path, "urls.txt")) as fid:
        urls = fid.readlines()
        urls = [line.strip() for line in urls]

    template = os.path.join(path, "template")
    index_uid = os.path.basename(os.path.dirname(path))

    # load and render the template
    temp_config_file = get_temp_file_name(".json")
    render_template(template, urls, temp_config_file, index_uid=index_uid)

    # Scrape it!
    #
    # this must be run as a system command as twisted will complain:
    # twisted.internet.error.ReactorNotRestartable
    #
    # Plus, it generates a ton of output.
    if verbose:
        result = subprocess.run(
            ["python", "-m", "scraper", temp_config_file],
        )
    else:
        result = subprocess.run(
            ["python", "-m", "scraper", temp_config_file], stdout=subprocess.PIPE
        )
        output = result.stdout.decode("utf-8")
        print(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape a single URL.")
    parser.add_argument("path", type=str, help="TODO")

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

    args = parser.parse_args()

    if args.meilisearch_host_url is not None:
        os.environ["MEILISEARCH_HOST_URL"] = args.meilisearch_host_url
    if args.meilisearch_api_key is not None:
        os.environ["MEILISEARCH_API_KEY"] = args.meilisearch_api_key

    print("Scrapping:")
    print(f"Directory:  {args.path}")
    # print(f"Index UID: {index_uid}")
    n_hits = scrape_from_directory(args.path, verbose=True)
