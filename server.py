"""
Local Web Server for Survey Analytics Dashboard
Serves the dashboard locally and automatically opens it in your default web browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable aggressive caching for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Try port 8080 or next available
    port = PORT
    for attempt in range(5):
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                url = f"http://localhost:{port}/index.html"
                print(f"=====================================================")
                print(f"  VEYRO Survey Analytics Dashboard & Sheet Converter")
                print(f"=====================================================")
                print(f"[*] Server running at: {url}")
                print(f"[*] Opening browser automatically...")
                print(f"[*] Press Ctrl+C in this terminal to stop the server.")
                print(f"=====================================================")
                
                webbrowser.open(url)
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Server stopped.")
        sys.exit(0)
