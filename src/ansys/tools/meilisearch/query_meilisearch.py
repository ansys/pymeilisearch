"""
Query a meilisearch host for a index and return it.

This can also be used to assert that documents exist within that index and to
delete it for testing.

"""

import os

import meilisearch


def main(index_uid):
    """Return the index given a meilisearch index_uid."""

    key = os.environ.get("MEILISEARCH_API_KEY")
    if key is None:
        raise RuntimeError("Environment variable `MEILISEARCH_API_KEY` is missing")

    url = os.environ.get("MEILISEARCH_HOST_URL")
    if url is None:
        raise RuntimeError("Environment variable `MEILISEARCH_HOST_URL` is missing")

    client = meilisearch.Client(url, key)
    return client.index(index_uid)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check if the number of documents in a meilisearch index is greater than 10"
    )
    parser.add_argument("index_uid", type=str, help="The index to query")

    parser.add_argument(
        "--delete",
        required=False,
        action="store_true",
        help="Remove the index",
    )

    args = parser.parse_args()

    index_uid = args.index_uid.replace("/", "-")
    index = main(index_uid)

    stats = index.get_stats()
    print("API reports index has {stats.number_of_documents} documents")
    assert stats.number_of_documents > 10

    if args.delete:
        print("Deleting index {index_uid}")
        index.delete()
