from unittest.mock import Mock, patch

from github import Github
import pytest

from ansys.tools.meilisearch.create_indexes import create_sphinx_indexes, get_sphinx_urls
from ansys.tools.meilisearch.get_pages import GitHubPages
from ansys.tools.meilisearch.scrapper import WebScraper
from ansys.tools.meilisearch.templates.utils import is_sphinx


@pytest.fixture(scope="module")
def orgs():
    return ["pyansys"]


@pytest.fixture
def github_pages():
    return GitHubPages("pyansys", token="my-token", ignore_githubio=True)


def test_get_repos(github_pages):
    with patch.object(Github, "get_organization") as mock_get_organization:
        mock_organization = Mock()
        mock_organization.get_repos.return_value = ["repo1", "repo2"]
        mock_get_organization.return_value = mock_organization

        repos = github_pages._get_repos()

        mock_get_organization.assert_called_once_with("pyansys")
        mock_organization.get_repos.assert_called_once()
        assert repos == ["repo1", "repo2"]


def test_has_github_pages(github_pages):
    mock_repo = Mock()
    response = {"public": True, "cname": "https://github.com/ansys/ansys-sphinx-theme"}
    verify_page = github_pages._has_github_pages(response, mock_repo)
    assert verify_page is True


def test_has_github_pages_bad_credentials(github_pages):
    mock_repo = Mock()
    mock_repo.has_pages = True
    response = {"message": "Bad credentials"}

    with patch("requests.get") as mock_requests_get:
        mock_requests_get.return_value = Mock()

        with pytest.raises(RuntimeError, match="Bad credentials"):
            github_pages._has_github_pages(response, mock_repo)


@pytest.fixture(scope="module")
def scraper_mock():
    with patch.object(WebScraper, "scrape_url") as mock_scraper:
        yield mock_scraper


@pytest.fixture(scope="module")
def public_urls():
    return {
        "pyansys/dev-guide ": "https://dev.docs.pyansys.com",
        "pyansys/pyansys": "https://docs.pyansys.com",
        "pyansys/actions": "https://actions.docs.pyansys.com",
        "pyansys/pyseascape": "https://seascape.docs.pyansys.com",
    }


def test_get_sphinx_urls(public_urls):
    assert get_sphinx_urls(public_urls) == public_urls


@pytest.mark.parametrize(
    "url",
    [
        "https://dev.docs.pyansys.com",
        "https://docs.pyansys.com",
        "https://actions.docs.pyansys.com",
        "https://seascape.docs.pyansys.com",
    ],
)
def test_is_sphinx(url):
    assert is_sphinx(url)


def test_temp_index_swapping(meilisearch_client):
    test_url = {"ansys/ansys-sphinx-theme": "https://sphinxdocs.ansys.com"}
    create_sphinx_indexes(
        test_url,
        meilisearch_client.meilisearch_host_url,
        meilisearch_client.meilisearch_host_url,
    )
    stats = meilisearch_client.client.get_all_stats()
    print(stats)
    index_uids = list(stats["indexes"].keys())
    assert "ansys-ansys-sphinx-theme-sphinx-docs" in index_uids
