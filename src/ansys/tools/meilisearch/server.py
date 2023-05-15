import http.server
import os
import socketserver
import threading
import webbrowser

from ansys.tools.meilisearch.create_indexes import scrap_web_page


def _serve_website(directory, port):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    try:
        # Create an HTTP server
        httpd = socketserver.TCPServer(("", port), Handler)
        print(f"Serving directory {directory} at http://localhost:{port}")

    except Exception as e:
        print(f"Error serving directory: {e}")

    webbrowser.open(f"http://localhost:{port}/")
    httpd.serve_forever()


def _scrape_website(index_uid, templates, directory):
    urls = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)  # Use os.path.join() with root and file
                relative_path = file_path.replace(directory, "")  # Remove the directory path
                relative_path = relative_path.replace("\\", "/")  # Remove the directory path
                # Append the relative path to the base URL
                url = f"http://localhost:8001/doc/_build/html/{relative_path}"
                urls.append(url)

    print(urls)

    scrap_web_page(index_uid, urls, templates)


def local_host_scraping(index_uid, templates, directory=None, port=8000):
    if directory is None:
        directory = ""

    with threading.Thread(
        target=_serve_website, args=(directory, port)
    ) as website_thread, threading.Thread(
        target=_scrape_website, args=(index_uid, templates, directory)
    ) as scrape_thread:
        website_thread.start()
        scrape_thread.start()

        try:
            scrape_thread.join()
        except Exception as e:
            print("Error occurred while scraping the website:", str(e))
        finally:
            website_thread.join(timeout=5)
            if website_thread.is_alive():
                print("The website thread is still alive. Stopping the thread...")
                website_thread._stop()
