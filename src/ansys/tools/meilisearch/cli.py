"""Allows the cli module for ansys-meilisearch"""
import click

from ansys.tools.meilisearch import __version__
from ansys.tools.meilisearch.create_indexes import scrap_web_page
from ansys.tools.meilisearch.server import local_host_scraping


@click.group()
def main():
    """Ansys tool for scraping docs to meilisearch."""
    pass


@main.command()
@click.option("--template", required=True, help="Name of the template to use.")
@click.option(
    "--index", required=True, help="Name of the meilisearch index used to identify the content."
)
@click.option(
    "--port", required=False, default=8000, help="The port in which local host has to connect."
)
@click.argument("source", type=click.Choice(["html", "url"]))
@click.argument("location")
def upload(template, index, source, location, port=8001):
    """Upload files or a website using the specified template and index."""

    if source == "html":
        local_host_scraping(index, template, location, port=port)

    elif source == "url":
        scrap_web_page(index, location, template)

    else:
        click.echo(f"Invalid source: {source}. Must be 'html' or 'url'.")


@main.command()
def version():
    """Display current version."""
    print(f"ansys-tools-meilisearch {__version__}")
