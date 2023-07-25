"""Templates utilities module."""
import re

import requests


def get_template(url: str) -> str:
    """
    Get the template name for a web page.

    Parameters
    ----------
    url : str
        URL of the web page.

    Returns
    -------
    str
        Template name for the web page.
    """
    return "sphinx_pydata" if is_sphinx(url) else "default"


def get_redirected_url(html):
    """
    Get the URL that a web page is being redirected to.

    Parameters
    ----------
    html : str
        Web page to search for a redirected URL.

    Returns
    -------
    str or None
        URL that the page is being redirected to. If no redirection
        is present, ``None`` is returned.
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
        URL of the web page.

    Returns
    -------
    bool
        ``True`` if the page was built using Sphinx, ``False`` otherwise.
    """
    response = requests.get(url)
    html = response.text
    if "Redirecting" in html:
        return is_sphinx(get_redirected_url(html))
    return "sphinx" in html
