from unittest import mock

import pytest

from ansys.tools.meilisearch.templates.utils import get_template


@mock.patch("requests.get")
def test_check_url_starts_with_https(mock_get, scraper):
    with pytest.raises(ValueError):
        scraper._check_url("htt://dev.docs.pyansys.com/")


@mock.patch("requests.get")
def test_check_url_returns_non_200(mock_get, scraper):
    mock_get.return_value.status_code = 404
    with pytest.raises(RuntimeError):
        scraper._check_url("https://some.example.com/")


def test_load_and_render_template(scraper):
    url = "https://dev.docs.pyansys.com/"
    template = "my_template.json"
    index_uid = "my_index"
    temp_file = scraper._load_and_render_template(url, template, index_uid)
    assert temp_file.endswith(".json")


def test_parse_output_empty_output(scraper):
    output = ""
    n_hits = scraper._parse_output(output)
    assert n_hits == 0


def test_parse_output_valid_output(scraper):
    output = "Scraping https://dev.docs.pyansys.com/ ...\nFound 10"
    n_hits = scraper._parse_output(output)
    assert n_hits == 10


@mock.patch("subprocess.run")
def test_scrape_url_command(mock_run, scraper):
    mock_run.return_value.stdout = b"Scraping https://dev.docs.pyansys.com/ ...\nFound 10"
    temp_file = "temp_file.json"
    output = scraper._scrape_url_command(temp_file)
    assert output.strip() == "Scraping https://dev.docs.pyansys.com/ ...\nFound 10"


def test_scrape_url_valid_url(scraper):
    url = "https://dev.docs.pyansys.com/"
    index_uid = "my_index"
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = b"Scraping https://dev.docs.pyansys.com/ ...\nFound 10"
        n_hits = scraper.scrape_url(url, index_uid)
        assert n_hits == 10


def test_scrape_from_directory(scraper, tmpdir):
    urls_file = tmpdir.join("urls.txt")
    urls_file.write("https://dev.docs.pyansys.com/\nhttps://sphinxdocs.ansys.com/version/stable/")
    scraper._check_url("https://dev.docs.pyansys.com/")
    template = get_template("https://dev.docs.pyansys.com/")
    assert template == "sphinx_pydata"
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = b"Scraping https://dev.docs.pyansys.com/ ...\nFound 10"
        results = scraper.scrape_from_directory(tmpdir)
    assert len(results) == 1
    assert all(isinstance(n_hits, int) for n_hits in results.values())
