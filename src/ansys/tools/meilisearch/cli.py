"""Command Line Interface for meilisearch."""

import click

from ansys.tools.meilisearch import __version__, scrap_local


def scrape_page(template):
    """scrape the page based on given template.

    Parameters
    ----------
    template : str
        Name of the template to be used as basis for the project

    """
    scrap_local()


@click.group()
def main():
    """Ansys tool for scraping docs to meilisearch."""
    pass


@main.command()
def version():
    """Display current version."""
    print(f"ansys-tools-meilisearch {__version__}")


@main.group()
def upload():
    """Create a new project from desired template."""
    pass


@upload.group()
def from_html():
    """Upload from HTML using the specified template."""
    pass


@from_html.command()
def sphinx():
    scrap_local("sphinx-pydata")
