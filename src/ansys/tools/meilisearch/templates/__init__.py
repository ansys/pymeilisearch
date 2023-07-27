"""PyMeilisearch templates subpackage."""
import json
import pathlib
from typing import Union

from jinja2 import Template

DEFAULT_TEMPLATE = pathlib.Path(__file__).parent.resolve() / "default.json"
SPHINX_PYDATA_TEMPLATE = pathlib.Path(__file__).parent.resolve() / "sphinx_pydata.json"

STOP_SPHINX_URLS = [
    "_sources",
    "_downloads",
    "_static",
    "_images",
    ".doctree",
]
"""List of stop points when scrapping URLs."""


def render_template(
    template: str,
    urls: Union[str, list[str]],
    path_out: str,
    index_uid: str = None,
    stop_urls_default: str = None,
) -> str:
    """Render a docsearch Sphinx template for a URL.

    Parameters
    ----------
    template : str or pathlib.Path
        Path to the template file or the name of the template to use.
        If a name is specified, it must be a key in the ``TEMPLATES``
        dictionary.
    urls : str, list[str]
        One or more URLs to crawl. URLs must start with ``https://``.
    path_out : str
        Path to write the rendered template to.
    index_uid : str, default: None
        Unique name for the custom index to use. This unique name is the
        URL without the ``https://``. The default is ``None``, in which
        case the unique name of the first URL specified for the ``urls``
        parameter is used.
    stop_urls_default : list[str], default: ['_sources', '_downloads', '_static', '_images', '.doctree']
        A list of stop points when scraping URLs. If specified, crawling
        will stop when encountering any URL containing any of the strings
        in this list. The default is ['_sources', '_downloads', '_static', '_images', '.doctree'].

    Returns
    -------
    str
        Unique name of the custom index that is used.

    Raises
    ------
    FileNotFoundError
        If the template file cannot be found.
    ValueError
        If any of the URLs specified for the ``urls`` parameter do not
        start with ``https://``.

    """
    if template == "sphinx_pydata":
        template_path = SPHINX_PYDATA_TEMPLATE
    elif template == "default":
        template_path = DEFAULT_TEMPLATE
    else:
        template_path = pathlib.Path(template)

    if not template_path.exists():
        raise FileNotFoundError(f"Unable to locate a template at {template_path}.")

    if template == "sphinx_pydata":
        stop_urls = [f"{urls[-1].rstrip('/')}/{segment}" for segment in STOP_SPHINX_URLS]
        if stop_urls_default is not None:
            stop_urls.extend(
                f"{urls[-1].rstrip('/')}{stop_url_default}"
                for stop_url_default in stop_urls_default
            )
    else:
        stop_urls = [stop_urls_default]

    template_str = template_path.read_text()
    template = Template(template_str)

    # Ensure urls is a list
    if isinstance(urls, str):
        urls = [urls]

    # Use the first url as index_uid if none is provided
    if index_uid is None:
        index_uid = urls[0].replace("https://", "")

    # Add stop_urls to the url

    start_url = json.dumps(urls)
    stop_url = json.dumps(stop_urls)

    # Render the template
    rendered_template = template.render(index_uid=index_uid, start_url=start_url, stop_url=stop_url)

    # Write the rendered template to a file
    path_out = pathlib.Path(path_out)
    path_out.write_text(rendered_template)

    return index_uid
