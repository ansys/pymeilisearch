import os

import pytest


def test_check_url_starts_with_https(scraper):
    with pytest.raises(ValueError):
        scraper._check_url("htt://dev.docs.pyansys.com/")


def test_check_url_returns_non_200(scraper):
    with pytest.raises(RuntimeError):
        scraper._check_url("https://some.example.com/")


def test_load_and_render_template(scraper):
    url = "https://dev.docs.pyansys.com/"
    template = "sphinx_pydata"
    index_uid = "my_index"
    temp_file = scraper._load_and_render_template(url, template, index_uid)
    assert os.path.exists(temp_file)
    os.remove(temp_file)


def test_load_and_render_template_with_invalid_path(scraper):
    url = "https://dev.docs.pyansys.com/"
    template = "my_template.json"
    index_uid = "my_index"
    with pytest.raises(FileNotFoundError):
        scraper._load_and_render_template(url, template, index_uid)


def test_parse_output_empty_output(scraper):
    output = ""
    n_hits = scraper._parse_output(output)
    assert n_hits == 0


def test_parse_output_valid_output(scraper):
    output = "Scraping https://dev.docs.pyansys.com/ ...\nFound 10"
    n_hits = scraper._parse_output(output)
    assert n_hits == 10


def test_scrape_url_command(scraper):
    url = "https://dev.docs.pyansys.com/"
    template = "sphinx_pydata"
    index_uid = "my-index"
    temp_config_file = scraper._load_and_render_template(url, template, index_uid)
    output = scraper._scrape_url_command(temp_config_file)
    assert "Scraping https://dev.docs.pyansys.com/" in output
    assert "Found" in output
    os.remove(temp_config_file)


def test_scrape_url_valid_url(scraper):
    url = "https://dev.docs.pyansys.com/"
    index_uid = "my_index"
    n_hits = scraper.scrape_url(url, index_uid, verbose=True)
    assert isinstance(n_hits, int)


def test_scrape_from_directory(scraper, tmpdir):
    urls_file = tmpdir.join("urls.txt")
    urls_file.write("https://dev.docs.pyansys.com/\nhttps://sphinxdocs.ansys.com/version/stable/")
    results = scraper.scrape_from_directory(str(tmpdir), verbose=True)
    assert len(results) == 2
    assert all(isinstance(n_hits, int) for n_hits in results.values())
