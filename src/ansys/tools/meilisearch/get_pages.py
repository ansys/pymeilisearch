"""
Query for public GitHub pages.
"""
import os
import urllib.request
import warnings

from github import Github
import requests


class GitHubPages:
    def __init__(self, org_name, token=None, ignore_githubio=True):
        """Query GitHub for the public gh-pages in an organization.

        Parameters
        ----------
        org_name : str
            Name of the the GitHub organization.
        token : str, default: None
            GitHub API token to use for authentication.
        ignore_githubio : bool, default: True
            Whether to ignore any URL for a GitHub page with ``github.io``
            in it.
        """
        self._org_name = org_name
        self._token = token or os.environ.get("GITHUB_TOKEN")
        self._ignore_githubio = ignore_githubio

    @property
    def org_name(self):
        """Name of the GitHub organization."""
        return self._org_name

    def _connect_github_api(self):
        """Connect to the GitHub API.

        Returns
        -------
        ~github.Github
            GitHub object connected to the GitHub API.
        """
        return Github(login_or_token=self._token)

    def _get_repos(self):
        """Get all repositories in the GitHub organization.

        Returns
        -------
        list
            List of repositories in the GitHub organization.
        """
        return self._connect_github_api().get_organization(self.org_name).get_repos()

    def _get_gh_page_response(self, repo):
        """Get the settings for public pages for a repository.

        Parameters
        ----------
        repo : Repository
            Repository to get public page settings for.

        Returns
        -------
        dict
            Dictionary containing the repository's public page settings.

        Raises
        ------
        HTTPError
            If the repository does not have public GitHub pages.
        """
        if not repo.has_pages:
            warnings.warn(f"Repo {repo.full_name} has no pages")
            return {}

        # Get the Github Pages settings for the repo
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        request_url = f"https://api.github.com/repos/{self.org_name}/{repo.name}/pages"
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            warnings.warn(f"Error getting public pages for {repo.full_name}: {e}")

    def _has_github_pages(self, response, repo):
        """Verify the public pages for a repository.

        Parameters
        ----------
        repo : Repository
            Repository to verify public pages for.
        response : dict
            Dictionary containing the repository's public page settings.

        Returns
        -------
        bool
            ``True`` if a public GitHub pages for the repository exist and can be
            verified, ``False`` otherwise.

        Raises
        ------
        RuntimeError
            If the response indicates that the credentials are invalid.
        """

        # only public pages
        if "message" in response and "Bad credentials" == response["message"]:
            raise RuntimeError("Bad credentials")

        if not response["public"]:
            return False

        # Verify repository visibility
        if repo.visibility != "public":
            warnings.warn(f"{repo.full_name}: Public pages with {repo.visibility} repo")

        url = response["cname"] if response["cname"] else response["html_url"]
        if not url.startswith("https"):
            url = f"https://{url}"

        # ignore dev documentation
        if url.startswith("https://dev.") and not url.startswith("https://dev.docs"):
            return False
        if "github.io" in url and self._ignore_githubio:
            return False

        try:
            code = urllib.request.urlopen(url).getcode()
            if code == 200:
                return True
            else:
                warnings.warn(f"Received {code} for {repo.full_name} at {url}")
        except:
            warnings.warn(f"Invalid URL for {repo.full_name} at {url}")

        return False

    def get_public_pages(self):
        """Get the public pages in the repositories in a GitHub organization.

        Returns
        -------
        dict
            Dictionary containing full repository names and public GitHub URLs
            for the GitHub organization.
        """
        # Iterate over the repos
        repo_cnames = {}
        for repo in self._get_repos():
            if not repo.has_pages:
                warnings.warn(f"Repo {repo.full_name} has no pages")
                continue
            if repo.full_name.endswith("-redirect"):
                continue
            response = self._get_gh_page_response(repo)

            if not self._has_github_pages(response, repo):
                continue

            url = response["cname"] if response["cname"] else response["html_url"]
            if not url.startswith("https"):
                url = f"https://{url}"
            repo_cnames[repo.full_name] = url

        return repo_cnames
