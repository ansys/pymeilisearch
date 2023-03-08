import json
import os

from jinja2 import Template

THIS_PATH = os.path.abspath(__file__)


def render_template(template, urls, path_out, index_uid=None):
    """Render a docsearch sphinx template for a given URL.

    The index_uid will be the url without https:://

    Parameters
    ----------
    url : str
        URL to crawl. For example "https://mapdl.docs.pyansys.com/". Must start
        with "https://".

    path_out : str, default: ''
        Optional path out.

    """
    template_path = os.path.join("..", "config_templates", f"{template}.json")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Unable to locate sphinx template at {template_path}")
    with open(template_path) as fid:
        template = Template(fid.read())

    # Render the template with the desired values
    if isinstance(urls, str):
        urls = [urls]

    for url in urls:
        if not url.startswith("https://"):
            raise ValueError(f'`url` {url} must start with "https://"')

    if index_uid is None:
        index_uid = urls[0].replace("https://", "")

    start_url = json.dumps(urls)

    rendered_template = template.render(index_uid=index_uid, start_url=start_url)

    # Write the rendered template to a new file
    with open(path_out, "w") as f:
        f.write(rendered_template)

    return index_uid
