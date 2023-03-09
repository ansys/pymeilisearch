import json
import pathlib
from typing import Union

from jinja2 import Template

# Declare the fundamental paths of the theme
THIS_PATH = pathlib.Path(__file__).parent.resolve()


def render_template(
    template: str, urls: Union[str, list[str]], path_out: str, index_uid: str = None
) -> str:
    """Render a docsearch sphinx template for a given URL.

    The index_uid will be the url without https:://

    Parameters
    ----------
    template : str
        Name of the template to use. Must be a JSON file located in the same directory as this script.
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
    template_path = THIS_PATH / f"{template}.json"
    if not template_path.is_file():
        raise FileNotFoundError(f"Unable to locate a template at {template_path}")

    with open(template_path) as f:
        template_str = f.read()

    template = Template(template_str)

    # Ensure urls is a list
    if isinstance(urls, str):
        urls = [urls]

    # Ensure all urls start with "https://"
    for url in urls:
        if not url.startswith("https://"):
            raise ValueError(f"`url` {url} must start with 'https://'")

    # Use the first url as index_uid if none is provided
    if index_uid is None:
        index_uid = urls[0].replace("https://", "")

    start_url = json.dumps(urls)

    # Render the template
    rendered_template = template.render(index_uid=index_uid, start_url=start_url)

    # Write the rendered template to a file
    with open(path_out, "w") as f:
        f.write(rendered_template)

    return index_uid
