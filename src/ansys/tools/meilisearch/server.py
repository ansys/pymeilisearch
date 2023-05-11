import http.server
import os
import socketserver


def local_host_scraping(index_uid, templates, directory=None, port=8000):
    if directory is None:
        directory = ""

    Handler = http.server.SimpleHTTPRequestHandler
    try:
        os.chdir(directory)
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving directory {directory} at port {port}")
            httpd.serve_forever()

            print("server stated")

            # Scrape the web page
            # scrap_web_page(index_uid, f"http://localhost:{port}", templates)

    except Exception as e:
        print(f"Error serving directory: {e}")
