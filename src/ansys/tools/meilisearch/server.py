import http.server
import os
import socketserver
import threading
import webbrowser

from ansys.tools.meilisearch.create_indexes import scrap_web_page


def _serve_website(directory, port):
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        os.chdir(directory)
        # Create an HTTP server
        httpd = socketserver.TCPServer(("", port), Handler)
        print(f"Serving directory {directory} at http://localhost:{port}")

    except Exception as e:
        print(f"Error serving directory: {e}")

    webbrowser.open(f"http://localhost:{port}/")
    httpd.serve_forever()


def _scrape_website(index_uid, templates, port):
    # scrapper = WebScraper()
    # temp_config_file = scrapper._load_and_render_template
    # (f"http://localhost:{port}/", templates, index_uid)
    # output = scrapper._scrape_url_command(temp_config_file)
    # n_hits = scrapper._parse_output(output)
    scrap_web_page(index_uid, f"http://localhost:{port}", templates)


def local_host_scraping(index_uid, templates, directory=None, port=8000):
    if directory is None:
        directory = ""

    # Start serving the website in a separate thread
    website_thread = threading.Thread(target=_serve_website, args=(directory, port))
    website_thread.start()

    # Scrape the website in a separate thread
    scrape_thread = threading.Thread(target=_scrape_website, args=(index_uid, templates, port))
    scrape_thread.start()

    # Wait for the scraping to complete
    scrape_thread.join()

    # Stop serving the website
    website_thread.join()
