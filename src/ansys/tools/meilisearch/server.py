import http.server
import os
import socketserver
import threading

from ansys.tools.meilisearch.create_indexes import scrap_web_page


def _serve_website(directory, port):
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = None  # Initialize httpd to None

    try:
        os.chdir(directory)
        # Create an HTTP server
        httpd = socketserver.TCPServer(("", port), Handler)
        print(f"Serving directory {directory} at http://localhost:{port}")
    except Exception as e:
        print(f"Error serving directory: {e}")
        return  # Exit the function if an exception occurs

    return httpd


def _scrape_website(index_uid, templates, directory, port):
    base_url = f"http://localhost:{port}"
    files = directory.rglob("*.html")
    urls = []
    for file in files:
        relative_path = str(file.relative_to(directory)).replace("\\", "/")
        urls.append(f"{base_url}/{relative_path}")

    print(urls)

    scrap_web_page(index_uid, urls, templates)


def local_host_scraping(index_uid, templates, directory, port):
    # Start serving the website in a separate thread
    http = _serve_website(directory, port)
    website_thread = threading.Thread(target=http.serve_forever)
    website_thread.start()

    # Scrape the website in a separate thread
    scrape_thread = threading.Thread(
        target=_scrape_website, args=(index_uid, templates, directory, port)
    )
    scrape_thread.start()

    # Wait for the scraping to complete
    scrape_thread.join()

    # Stop serving the website
    http.shutdown()
    website_thread.join()
