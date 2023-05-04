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
def html():
    """Upload from HTML using the specified template."""
    pass


@html.command()
@click.option("--template", default="sphinx-pydata", help="The template to use.")
@click.option("--index", help="The index uid to use", required=True)
@click.argument("path", type=click.Path(exists=True))
def upload_html(template, index, path):
    scrape_page(template, path)
    print(f"HTML files at {path} uploaded to index {index} using template {template}.")


@upload.group()
def web():
    """Upload from HTML using the specified template."""
    pass


@web.command()
@click.option("--template", default="sphinx-pydata", help="The template to use.")
@click.option("--index", help="The index uid to use", required=True)
@click.argument("url")
def upload_web(template, index, url):
    scrape_page(template, url)
    print(f"Web page at {url} uploaded to index {index} using template {template}.")


@upload.group()
def github():
    """Upload from GitHub using the specified template."""
    pass


@github.command()
@click.option("--template", default="sphinx-pydata", help="The template to use.")
@click.option("--index", help="The index uid to use", required=True)
@click.argument("repo")
def upload_github(template, index, repo):
    scrape_page(template, repo)
    print(f"GitHub repository {repo} uploaded to index {index} using template {template}.")
