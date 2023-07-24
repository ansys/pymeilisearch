import platform

import docker
import pytest
import requests

from ansys.tools.meilisearch.client import MeilisearchClient
from ansys.tools.meilisearch.scrapper import WebScraper


@pytest.fixture(scope="session")
def meilisearch_client(meilisearch_container):
    meilisearch_client = MeilisearchClient(
        meilisearch_host_url="http://localhost:7700", meilisearch_api_key="masterKey"
    )
    return meilisearch_client


@pytest.fixture(scope="function")
def scraper(meilisearch_client):
    return WebScraper(
        meilisearch_client.meilisearch_host_url, meilisearch_client.meilisearch_host_url
    )


@pytest.fixture(scope="session")
def meilisearch_container():
    image_name = "getmeili/meilisearch:latest"
    container_port = 7700

    if platform.system() == "Windows":
        base_url = "npipe:////./pipe/docker_engine"
    else:
        base_url = "unix://var/run/docker.sock"

    # Create a Docker client
    docker_client = docker.from_env()

    containers_with_port = [
        container for container in docker_client.containers.list(filters={"expose": container_port})
    ]
    existing_container = containers_with_port[0] if containers_with_port else None

    if existing_container:
        return existing_container

    # Pull the Meilisearch image
    docker_client.images.pull(image_name)

    # Create and start the Meilisearch container
    container = docker_client.containers.run(
        image=image_name,
        ports={f"{container_port}/tcp": container_port},
        detach=True,
        name="meilisearch-container",
    )

    # Wait for Meilisearch to be ready
    url = f"http://localhost:{container_port}/health"
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
