"""
Query for public github pages.
"""
import os
import urllib.request
import warnings

from github import Github
import requests


def public_gh_pages(org_name, token=None, ignore_githubio=True):
    """Query GitHub for the public gh-pages in an organization.

    Parameters
    ----------
    org_name : str
        GitHub organization name.

    ignore_githubio : bool, default: True
        Ignore any GitHub page url with github.io in it.

    Returns
    -------
    dict
        Dictionary containing the full repository name and the public github
        URLs.

    """
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")
    if token is None:
        raise RuntimeError('Missing "GITHUB_TOKEN" environment variable.')

    # Connect to the GitHub API
    github = Github(login_or_token=token)

    # Get all repos in the organization
    repos = github.get_organization(org_name).get_repos()

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Iterate over the repos
    repo_cnames = {}
    for repo in repos:
        # Get the Github Pages settings for the repo

        if repo.full_name.endswith("-redirect"):
            continue

        # Check if the custom domain is set for the repo's Github Pages
        if not repo.has_pages:
            continue
        request_url = f"https://api.github.com/repos/{org_name}/{repo.name}/pages"
        response = requests.get(request_url, headers=headers)
        out = response.json()

        # only public pages
        if "message" in out:
            if "Bad credentials" == out["message"]:
                raise RuntimeError("Bad credentials")

        if not out["public"]:
            continue

        # verify
        if repo.visibility != "public":
            warnings.warn(f"{repo.full_name}: Public pages with {repo.visibility} repo")

        url = out["cname"] if out["cname"] else out["html_url"]
        if not url.startswith("https"):
            url = f"https://{url}"

        # ignore dev documentation
        if url.startswith("https://dev.") and not url.startswith("https://dev.docs"):
            continue
        if "github.io" in url and ignore_githubio:
            continue

        try:
            code = urllib.request.urlopen(url).getcode()
            if code == 200:
                repo_cnames[repo.full_name] = url
            else:
                warnings.warn(f"Received {code} for {repo.full_name} at {url}")
        except:
            warnings.warn(f"Invalid URL for {repo.full_name} at {url}")

    return repo_cnames
