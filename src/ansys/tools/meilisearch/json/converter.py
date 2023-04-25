import json

from bs4 import BeautifulSoup

# Read the HTML file
with open("index.html", "r") as f:
    html = f.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extract the data from the HTML
data_js = {}

index_uid = "test"

# Example: Extract the title of the page
title = soup.title.string

data_js["index_uid"] = index_uid

data_js["lvl0"] = title

h1_elements = []
for h1 in soup.find_all("h1"):
    h1_elements.append(h1.get_text())
data_js["lvl1"] = h1_elements

h2_elements = []
for h2 in soup.find_all("h2"):
    h2_elements.append(h2.get_text())
data_js["lvl2"] = h2_elements

h3_elements = []
for h3 in soup.find_all("h3"):
    h3_elements.append(h3.get_text())
data_js["lvl3"] = h3_elements

h4_elements = []
for h4 in soup.find_all("h4"):
    h4_elements.append(h4.get_text())
data_js["lvl4"] = h4_elements

h5_elements = []
for h5 in soup.find_all("h5"):
    h5_elements.append(h5.get_text())
data_js["lvl5"] = h5_elements

h6_elements = []
for h6 in soup.find_all("h6"):
    h6_elements.append(h6.get_text())
data_js["lvl6"] = h6_elements

# Example: Extract all paragraphs and store them in an array
paragraphs = []
for p in soup.find_all("p"):
    paragraphs.append(p.get_text())
data_js["text"] = paragraphs

# Write the data to a JSON file
with open("data.json", "w") as f:
    json.dump(data_js, f)
