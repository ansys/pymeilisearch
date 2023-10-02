import os

import pytest


def test_check_url_starts_with_https(scraper):
    with pytest.raises(ValueError):
        scraper._check_url("htt://dev.docs.pyansys.com/")


def test_check_url_returns_non_200(scraper):
    with pytest.raises(RuntimeError):
        scraper._check_url("http://dev.docs.pyansys.com/version/stable/example")


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
