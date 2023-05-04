import click

from ansys.tools.meilisearch import __version__, scrap_local


def scrape_page(template, path):
    """scrape the page based on given template.

    Parameters
    ----------
    template : str
        Name of the template to be used as basis for the project
    path : str
        Path to HTML files to be uploaded

    """
    scrap_local(template, path)


@click.group()
def main():
    """Ansys tool for scraping docs to meilisearch."""
    pass


@main.command()
@click.option('--template', required=True, help='Name of the template to use.')
@click.option('--index', required=True, help='Name of the meilisearch index used to identify the content.')
@click.argument('source', type=click.Choice(['html', 'url']))
@click.argument('location')
def upload(template, index, source, location):
    """Upload files or a website using the specified template and index."""
    if source == 'html':
        click.echo(f"Uploading HTML files using template '{template}' and index '{index}':")
        click.echo(f"- Location: {location}")
        # Add your upload code for HTML files here.
    elif source == 'url':
        click.echo(f"Uploading website using template '{template}' and index '{index}':")
        click.echo(f"- URL: {location}")
        # Add your upload code for websites here.
    else:
        click.echo(f"Invalid source: {source}. Must be 'html' or 'url'.")


@main.command()
def version():
    """Display current version."""
    print(f"ansys-tools-meilisearch {__version__}")

