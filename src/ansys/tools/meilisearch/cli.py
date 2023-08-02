"""PyMeilisearch CLI module."""
import os
import pathlib

import click

from ansys.tools.meilisearch import __version__
from ansys.tools.meilisearch.create_indexes import (
    create_sphinx_indexes,
    get_public_urls,
    get_sphinx_urls,
    scrap_web_page,
)
from ansys.tools.meilisearch.server import local_host_scraping


@click.group()
def main():
    """Provides the CLI tool for scraping documents or a website for uploading to Meilisearch."""
    pass


@main.command()
@click.option(
    "--template",
    required=True,
    help="Name of the template to use or the path where the template is located. Available templates are ``sphinx_pydata`` and ``default``.",  # noqa: E501
)
@click.option(
    "--index", required=True, help="Name of the Meilisearch index to use to identify the content."
)
@click.option("--cname", required=False, default="", help="The CNAME that hosts the documents.")
@click.option("--port", required=False, default=8000, help="Port number for serving the pages.")
@click.option(
    "--orgs",
    required=False,
    default=[],
    help="GitHub organizations to scrape public URLs from.",
    multiple=True,
)
@click.option(
    "--stop_urls",
    required=False,
    default=[],
    help="The stop urls to stop scraping.",
    multiple=True,
)
@click.argument("source", type=click.Choice(["html", "url", "github"]))
@click.argument("location")
def upload(template, index, source, location, cname, port, orgs, stop_urls):
    """Upload documents or a website using a template and index.

    Parameters
    ----------
    template : str
        Name of the template to use or the path to where the template
        file is located. Available templates are ``sphinx_pydata`` and ``default``.
    index : str
        Name of the Meilisearch index to use to identify the content.
    source : str
        Format type for the documents to upload. Options are ``html``, ``url``,
        and ``github``.
    location : str
        Location of the documents or website to upload.
    cname : str
        CNAME that hosts the documents. While supplying a CNAME
        is optional, doing so is recommended for scraping documents
        on the local host.
    port : int
        Port that the localhost is connected on.
    orgs : str or list[str]
        One or more GitHub organizations to scrape public GitHub pages from.
    stop_urls : str or list[str], default: None
        A list of stop points when scraping URLs. If specified, crawling
        will stop when encountering any URL containing any of the strings
        in this list.

    Notes
    -----
    Ensure that these environment variables are set:

    - ``MEILISEARCH_HOST_URL``: URL for the Meilisearch host
    - ``MEILISEARCH_API_KEY``: API key (admin) for the Meilisearch host
    - ``GH_PUBLIC_TOKEN``: GitHub token for the organization
      (if running in a GitHub CI/CD environment)
    """

    if source == "html":
        location = pathlib.Path.cwd() / location
        os.environ["DOCUMENTATION_CNAME"] = cname
        os.environ["DOCUMENTATION_PORT"] = str(port)
        local_host_scraping(index, template, location, port, stop_urls)

    elif source == "url":
        scrap_web_page(index, location, template, stop_urls)

    elif source == "github":
        public_gh_pages_urls = get_public_urls(orgs)
        if template == "sphinx_pydata":
            urls = get_sphinx_urls(public_gh_pages_urls)
            create_sphinx_indexes(urls, stop_urls)
        else:
            create_sphinx_indexes(public_gh_pages_urls, stop_urls)

    else:
        click.echo(f"Invalid source: {source}. Must be 'html', 'url', or 'github'.")


@main.command()
def version():
    """Get the version of your PyMeilisearch installation."""
    print(f"PyMeilisearch {__version__}")
