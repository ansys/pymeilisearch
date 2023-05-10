import http.server
import socketserver

from ansys.tools.meilisearch.create_indexes import scrap_web_page


def local_host_scraping(index_uid, templates, directory=None):
    if directory is None:
        # Use the current working directory
        directory = ""

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT} from {directory}")
        httpd.serve_forever()

    scrap_web_page(index_uid, "http://localhost:8000/", templates)
