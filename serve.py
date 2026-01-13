import http.server
import socketserver

PORT = 3000

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
except OSError as e:
    if e.errno == 48:
        print(f"Port {PORT} is already in use. Please kill the process using it or try a different port.")
    else:
        print(f"Error: {e}")
