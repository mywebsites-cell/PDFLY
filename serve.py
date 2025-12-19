#!/usr/bin/env python3
"""
Simple static server with clean-URL support for the frontend directory.

Usage: python serve.py [port]

Behavior:
- Requests for "/" or "/home" -> serves `frontend/index.html`
- Requests without an extension (e.g. `/merge-pdf`) -> serves `frontend/merge-pdf.html` if exists
- Requests for files with extensions are served normally from `frontend/`
"""
import http.server
import socketserver
import os
import sys
from urllib.parse import unquote, urlparse

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.join(os.path.dirname(__file__), 'frontend')


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Based on SimpleHTTPRequestHandler.translate_path but rooted to FRONTEND
        parsed = urlparse(path)
        path = unquote(parsed.path)
        if path == '/' or path.lower() == '/home':
<<<<<<< HEAD
<<<<<<< HEAD
            # Serve the project root index.html (moved out of frontend)
            return os.path.join(os.path.dirname(__file__), 'index.html')
=======
            requested = 'index.html'
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
=======
            requested = 'index.html'
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
        else:
            # strip leading /
            requested = path.lstrip('/')
            if '.' not in os.path.basename(requested):
                alt = requested + '.html'
                alt_full = os.path.join(ROOT, alt)
                if os.path.exists(alt_full):
                    requested = alt
        full_path = os.path.join(ROOT, requested)
        return full_path

    def do_GET(self):
        # Redirect requests that explicitly include .html to the clean path
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # If request is for root or index.html -> redirect to /home
        if path == '/' or path.lower().endswith('/index.html') or path.lower() == '/index.html':
            self.send_response(301)
            self.send_header('Location', '/home')
            self.end_headers()
            return

        # If request ends with .html (and is not an asset), redirect to path without extension
        if path.endswith('.html'):
            clean = path[:-5] or '/'
            self.send_response(301)
            self.send_header('Location', clean)
            self.end_headers()
            return

        # Otherwise, fall back to serving files; allow extensionless mapping to .html
        return super().do_GET()

    def log_message(self, format, *args):
        # keep logs concise
        sys.stdout.write("[serve] %s - - %s\n" % (self.client_address[0], format%args))


if __name__ == '__main__':
    os.chdir(ROOT)
    handler = CleanURLHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving frontend from {ROOT} at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")