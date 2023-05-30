import json
import pathlib
from typing import Union

from jinja2 import Template

TEMPLATES = {
    "default": "default.json",
    "sphinx_pydata": "sphinx_pydata.json",
}

STOP_SPHINX_URLS = [
    "_sources",
    "_downloads",
    "_static",
    "_images",
    ".doctree",
]


def render_template(
    template: str,
    urls: Union[str, list[str]],
    path_out: str,
    index_uid: str = None,
    stop_urls_default: str = None,
) -> str:
    """Render a docsearch sphinx template for a given URL.

    The index_uid will be the url without https:://

    Parameters
    ----------
    template : str
        Name of the template to use. Must be a key in the TEMPLATES dictionary.
    urls : str or list of str
        URL(s) to crawl. Must start with "https://".
    path_out : str
        Path to write the rendered template to.
    index_uid : str, default: The index uid of first url in list
        Custom index uid to use.

    Returns
    -------
    str
        The index_uid used.

    Raises
    ------
    FileNotFoundError
        If the template file cannot be found.
    ValueError
        If any of the URLs do not start with "https://".

    """
    template_path = pathlib.Path(__file__).parent.resolve() / TEMPLATES.get(
        template, "default.json"
    )

    if not template_path.exists():
        raise FileNotFoundError(f"Unable to locate a template at {template_path}")

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
