"""
Query for public github pages.
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
            GitHub organization name.

        token : str, default: None
            The GitHub API token to use for authentication.

        ignore_githubio : bool, default: True
            Ignore any GitHub page url with github.io in it.
        """
        self._org_name = org_name
        self._token = token or os.environ.get("GITHUB_TOKEN")
        self._ignore_githubio = ignore_githubio

    @property
    def org_name(self):
        """Returns the organization name."""
        return self._org_name

    def _connect_github_api(self):
        """Connect to the GitHub API.

        Returns
        -------
        Github
            A Github object connected to the GitHub API.
        """
        return Github(login_or_token=self._token)

    def _get_repos(self):
        """Get all repos in the organization.

        Returns
        -------
        list of Repository
            A list of Repository objects.
        """
        return self._connect_github_api().get_organization(self.org_name).get_repos()

    def _has_github_pages(self, repo):
        """Verify the public pages for a given repo.

        Parameters
        ----------
        repo : Repository
            The Repository object to check.

        Returns
        -------
        str or False
            The URL of the public pages, or ``False`` if they do not exist or could not be verified.
        """
        if not repo.has_pages:
            return False

        # Get the Github Pages settings for the repo
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        request_url = f"https://api.github.com/repos/{self.org_name}/{repo.name}/pages"
        response = requests.get(request_url, headers=headers)
        out = response.json()

        # only public pages
        if "message" in out and "Bad credentials" == out["message"]:
            raise RuntimeError("Bad credentials")

        if not out["public"]:
            return False

        # verify
        if repo.visibility != "public":
            warnings.warn(f"{repo.full_name}: Public pages with {repo.visibility} repo")

        url = out["cname"] if out["cname"] else out["html_url"]
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
                return url
            else:
                warnings.warn(f"Received {code} for {repo.full_name} at {url}")
        except:
            warnings.warn(f"Invalid URL for {repo.full_name} at {url}")

        return False

    def get_public_pages(self):
        """Query GitHub for the public gh-pages in an organization.

        Returns
        -------
        dict
            Dictionary containing the full repository name and the public github
            URLs.
        """
        # Iterate over the repos
        repo_cnames = {}
        for repo in self._get_repos():
            if repo.full_name.endswith("-redirect"):
                continue

            url = self._has_github_pages(repo)
            if url:
                repo_cnames[repo.full_name] = url

        return repo_cnames
