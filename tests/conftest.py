import os
import platform

import docker
import pytest
import requests

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.scraper import WebScraper


@pytest.fixture(scope="session")
def meilisearch_client(meilisearch_container, meilisearch_port):
    meilisearch_client = MeilisearchClient(
        meilisearch_host_url=f"http://localhost:{meilisearch_port}", meilisearch_api_key="masterKey"
    )
    return meilisearch_client


@pytest.fixture(scope="function")
def scraper(meilisearch_client, meilisearch_port):
    return WebScraper(
        meilisearch_host_url=f"http://localhost:{meilisearch_port}", meilisearch_api_key="masterKey"
    )


@pytest.fixture(scope="session")
def meilisearch_port():
    default_port = 7700
    return int(os.environ.get("MEILISEARCH_PORT", default_port))


@pytest.fixture(scope="session")
def meilisearch_container(meilisearch_port):
    image_name = "getmeili/meilisearch:latest"

    if platform.system() == "Windows":
        base_url = "npipe:////./pipe/docker_engine"
    else:
        base_url = "unix://var/run/docker.sock"

    # Create a Docker client
    docker_client = docker.from_env()

    containers_with_port = [
        container
        for container in docker_client.containers.list(filters={"expose": meilisearch_port})
    ]
    existing_container = containers_with_port[0] if containers_with_port else None

    if existing_container:
        return existing_container

    # Pull the Meilisearch image
    docker_client.images.pull(image_name)

    # Create and start the Meilisearch container
    container = docker_client.containers.run(
        image=image_name,
        ports={f"{meilisearch_port}/tcp": meilisearch_port},
        detach=True,
        name="meilisearch-container",
    )

    # Wait for Meilisearch to be ready
    url = f"http://localhost:{meilisearch_port}/health"
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except (requests.RequestException, requests.ConnectionError):
            continue

    # yield the container
    yield container

    # Stop and remove
    container.stop()
    container.remove()
