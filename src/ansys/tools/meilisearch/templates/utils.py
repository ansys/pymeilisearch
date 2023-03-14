"""Provides the templates utils module."""
import re

import requests


def get_template(url):
    """
    Determine the template name for the given URL.

    Parameters
    ----------
    url : str
        The URL of the web page to check.

    Returns
    -------
    str
        The name of the template to use for the page, either "sphinx" if the
        page was built using Sphinx or "default" otherwise.
    """
    return "sphinx_pydata" if is_sphinx(url) else "default"


def get_redirected_url(html):
    """
    Extract the redirected URL from the given HTML.

    Parameters
    ----------
    html : str
        The HTML content to search for the redirected URL.

    Returns
    -------
    str or None
        The URL that the page is being redirected to, if there is one. If no
        redirection is present, returns None.
    """
    match = re.search(r'<meta http-equiv="refresh" content="0; URL=(.*?)">', html)
    if match:
        redirected_url = match.group(1)
        return redirected_url
    else:
        return None


def is_sphinx(url):
    """
    Determine if a web page was built using Sphinx.

    Parameters
    ----------
    url : str
        The URL of the web page to check.

    Returns
    -------
    bool
        True if the page was built using Sphinx, False otherwise.
    """
    response = requests.get(url)
    html = response.text
    if "Redirecting" in html:
        return is_sphinx(get_redirected_url(html))
    return "sphinx" in html
