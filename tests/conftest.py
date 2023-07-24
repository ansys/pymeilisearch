import pytest

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


from docker import APIClient
import pytest
import requests


@pytest.fixture(scope="session")
def meilisearch_container():
    # Define the image and port for the Meilisearch container
    image_name = "getmeili/meilisearch:latest"
    container_port = 7700

    # Create a Docker client
    docker_client = APIClient(base_url="unix://var/run/docker.sock")

    # Check if port 7700 is already in use on localhost
    containers = docker_client.containers(all=True)
    for container in containers:
        if "Ports" in container and container["Ports"]:
            for port_info in container["Ports"]:
                if "PublicPort" in port_info and port_info["PublicPort"] == container_port:
                    pytest.skip("Port 7700 is already in use. Skipping Docker tests.")

    # Pull the Meilisearch image
    docker_client.pull(image_name)

    # Create and start the Meilisearch container
    container = docker_client.create_container(
        image=image_name, ports=[container_port], detach=True
    )
    docker_client.start(container=container["Id"], port_bindings={container_port: container_port})

    # Wait for Meilisearch to be ready
    url = f"http://localhost:{container_port}/health"
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except (requests.RequestException, requests.ConnectionError):
            continue

    # Yield the container to the test
    yield container

    # Teardown: Stop and remove the container
    docker_client.stop(container=container["Id"])
    docker_client.remove_container(container["Id"])
