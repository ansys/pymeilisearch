import http.server
import os
import socketserver
import threading
import webbrowser

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

    webbrowser.open(f"http://localhost:{port}/")
    httpd.serve_forever()


def _scrape_website(index_uid, templates, directory, port):
    urls = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)  # Use os.path.join() with root and file
                relative_path = file_path.replace(directory, "")  # Remove the directory path
                relative_path = relative_path.replace("\\", "/")  # Remove the directory path
                # Append the relative path to the base URL
                url = f"http://localhost:{port}/{relative_path}"
                urls.append(url)

    print(urls)

    scrap_web_page(index_uid, urls, templates)


def local_host_scraping(index_uid, templates, directory=None, port=None):
    if directory is None:
        directory = ""

    print("===============================", port)

    # Start serving the website in a separate thread
    website_thread = threading.Thread(target=_serve_website, args=(directory, port))
    website_thread.start()

    # Scrape the website in a separate thread
    scrape_thread = threading.Thread(
        target=_scrape_website, args=(index_uid, templates, directory, port)
    )
    scrape_thread.start()

    # Wait for the scraping to complete
    scrape_thread.join()

    # Stop serving the website
    website_thread.join()
