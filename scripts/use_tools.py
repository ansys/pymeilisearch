from ansys.tools.meilisearch.all_doc_indexer import DocsAllPublic
from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.scrapper import WebScraper

# Scrape a single url will desired index
client = MeilisearchClient()
scrapper = WebScraper(client.meilisearch_host_url, client.meilisearch_api_key)
n_hits = scrapper.scrape_url("https://sphinxdocs.ansys.com/", "testing-index")
print(n_hits)


# Add all docs of particular index (org) to a single index
all_doc = DocsAllPublic(client, "testing-all")
all_doc.add_all_public_doc(["testing"])
client.client.index("temp-testing-all").delete()
