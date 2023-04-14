import argparse

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.create_indexes import create_sphinx_indexes, get_sphinx_urls


def create_filtered_sphinx_indexes(urls, client):
    filtered_sphinx_urls = get_sphinx_urls(urls)
    create_sphinx_indexes(
        filtered_sphinx_urls, client.meilisearch_host_url, client.meilisearch_api_key
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "function_name",
        choices=["create_filtered_sphinx_indexes"],
        help="Name of function to run",
    )
    args = parser.parse_args()

    client = MeilisearchClient()
    urls = {
        "pyansys/pyaedt": "https://aedt.docs.pyansys.com",
    }

    if args.function_name == "create_sphinx_indexes":
        create_filtered_sphinx_indexes(urls, client)
    else:
        raise ValueError("Invalid function name: {}".format(args.function_name))
