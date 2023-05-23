import http.server
import os
import socketserver
import threading

from ansys.tools.meilisearch.create_indexes import scrap_web_page


class WebsiteServer:
    """
    Website server that serves the specified directory on the given port.
    """

    def __init__(self, directory, port):
        """
        Initialize the WebsiteServer.

        Parameters
        ----------
        directory : str
            The directory to serve.
        port : int
            The port number to listen on.
        """
        self.directory = directory
        self.port = port
        self.httpd = None
        self.server_thread = None

    def serve_website(self):
        """
        Start serving the website.
        """
        Handler = http.server.SimpleHTTPRequestHandler

        try:
            os.chdir(self.directory)
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            print(f"Serving directory {self.directory} at http://localhost:{self.port}")
            self.httpd.serve_forever()
        except Exception as e:
            print(f"Error serving directory: {e}")
            if self.httpd:
                self.httpd.shutdown()

    def stop_serving(self):
        """
        Stop serving the website.
        """
        if self.httpd:
            self.httpd.shutdown()

    def start_serving(self):
        """
        Start serving the website in a separate thread.
        """
        self.server_thread = threading.Thread(target=self.serve_website)
        self.server_thread.start()

    def join(self):
        """
        Wait for the server thread to complete.
        """
        if self.server_thread:
            self.server_thread.join()


def scrape_website(index_uid, templates, directory, port):
    """
    Scrape the website by collecting the URLs of HTML files in the specified directory.

    Parameters
    ----------
    index_uid : str
        The index UID for MeiliSearch.
    templates : list
        List of templates.
    directory : str
        The directory containing the website.
    port : int
        The port number the website is served on.
    """
    base_url = f"http://localhost:{port}"
    files = directory.rglob("*.html")
    urls = [f"{base_url}/{file.relative_to(directory).as_posix()}" for file in files]

    scrap_web_page(index_uid, urls, templates)


def local_host_scraping(index_uid, templates, directory, port):
    """
    Perform local host scraping by serving the directory and scraping its content.

    Parameters
    ----------
    index_uid : str
        The index UID for MeiliSearch.
    templates : list
        List of templates.
    directory : str
        The directory to serve and scrape.
    port : int
        The port number to listen on.
    """
    # Start serving the website in a separate thread
    website_server = WebsiteServer(directory, port)
    website_server.start_serving()

    # Scrape the website
    scrape_website(index_uid, templates, directory, port)

    # Stop serving the website
    website_server.stop_serving()
    website_server.join()