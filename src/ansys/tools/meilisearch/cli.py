"""Allows the CLI module for pymeilisearch"""
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
    """Ansys tool for scraping docs to MeiliSearch."""
    pass


@main.command()
@click.option(
    "--template",
    required=True,
    help="Name of the template to use or specify the path where the template is located. Available templates are `sphinx_pydata` and `default`.",  # noqa: E501
)
@click.option(
    "--index", required=True, help="Name of the MeiliSearch index used to identify the content."
)
@click.option(
    "--cname", required=False, default="", help="The CNAME in which the documents are hosted."
)
@click.option("--port", required=False, default=8000, help="Port number for serving the pages.")
@click.option(
    "--orgs",
    required=False,
    default=[],
    help="The GitHub organizations from which public URLs are scraped.",
    multiple=True,
)
@click.argument("source", type=click.Choice(["html", "url", "github"]))
@click.argument("location")
def upload(template, index, source, location, cname, port, orgs):
    """Upload files or a website using the specified template and index.

    Notes
    -----
    Make sure to set the following environment variables:

    - ``MEILISEARCH_HOST_URL``: MeiliSearch hosted URL
    - ``MEILISEARCH_API_KEY``: MeiliSearch API key
    - ``GH_PUBLIC_TOKEN``: GitHub token for the organization (if running in a GitHub CI environment)
    """

    if source == "html":
        location = pathlib.Path.cwd() / location
        os.environ["DOCUMENTATION_CNAME"] = cname
        os.environ["DOCUMENTATION_PORT"] = str(port)
        local_host_scraping(index, template, location, port)

    elif source == "url":
        scrap_web_page(index, location, template)

    elif source == "github":
        public_gh_pages_urls = get_public_urls(orgs)
        if template == "sphinx-pydata":
            urls = get_sphinx_urls(public_gh_pages_urls)
            create_sphinx_indexes(urls)
        else:
            create_sphinx_indexes(public_gh_pages_urls)

    else:
        click.echo(f"Invalid source: {source}. Must be 'html', 'url', or 'github'.")


@main.command()
def version():
    """Display current version."""
    print(f"pymeilisearch {__version__}")
