import json
import pathlib

from ansys.tools.meilisearch.json.default import DefaultStrategy

# Declare the fundamental paths of the theme
DEFAULT_TEMPLATE = pathlib.Path(__file__).parent.resolve() / "default.json"
html = pathlib.Path(__file__).parent.resolve() / "index.html"
# Open the file
with open(DEFAULT_TEMPLATE) as f:
    # Load the data from the file into a dictionary
    data = json.load(f)

with open(html, "r") as f:
    html = f.read()

record = DefaultStrategy(data, html)
print(record.get_records_from_dom())
