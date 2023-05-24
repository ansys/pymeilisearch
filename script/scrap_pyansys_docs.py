import argparse

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.create_indexes import (
    create_sphinx_indexes,
    get_public_urls,
    get_sphinx_urls,
)


def filter_urls(urls_to_filter, long_urls, urls):
    filtered_urls_to_filter = dict(urls_to_filter)
    filtered_urls_to_filter[
        "pyansys/pyedb"
    ] = "https://aedt.docs.pyansys.com/version/stable/EDBAPI/"
    filter_url = {title: url for title, url in urls.items() if title not in filtered_urls_to_filter}
    return {title: url for title, url in filter_url.items() if title not in long_urls}


def create_filtered_sphinx_indexes(filtered_urls, client):
    filtered_sphinx_urls = get_sphinx_urls(filtered_urls)
    create_sphinx_indexes(
        filtered_sphinx_urls, client.meilisearch_host_url, client.meilisearch_api_key
    )


def create_pyaedt_sphinx_indexes(urls, client):
    filtered_sphinx_urls = get_sphinx_urls(urls)
    create_sphinx_indexes(
        filtered_sphinx_urls,
        client.meilisearch_host_url,
        client.meilisearch_api_key,
        is_pyaedt=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "function_name",
        choices=[
            "create_filtered_sphinx_indexes",
            "create_pyaedt_sphinx_indexes",
            "create_long_urls",
        ],
        help="Name of function to run",
    )
    args = parser.parse_args()

    client = MeilisearchClient()
    urls = {
        "ansys/pyaedt": "https://aedt.docs.pyansys.com",
    }
    long_urls = {
        "ansys/pymapdl": "https://mapdl.docs.pyansys.com",
        "ansys/pydpf-core": "https://dpf.docs.pyansys.com",
        "ansys/pyfluent": "https://fluent.docs.pyansys.com",
    }
    if args.function_name == "create_filtered_sphinx_indexes":
        orgs = ["ansys", "ansys-internal"]
        public_gh_pages = get_public_urls(orgs)
        filtered_urls = filter_urls(dict.fromkeys(urls.keys()), long_urls, public_gh_pages)
        create_filtered_sphinx_indexes(filtered_urls, client)
    elif args.function_name == "create_pyaedt_sphinx_indexes":
        create_pyaedt_sphinx_indexes(urls, client)

    elif args.function_name == "create_long_urls":
        create_filtered_sphinx_indexes(long_urls, client)
    else:
        raise ValueError("Invalid function name: {}".format(args.function_name))
