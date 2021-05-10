
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import ssl
import shutil
import os

#openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj /CN=localhost
class Test(SimpleHTTPRequestHandler):
    def connect(self):
        print("TEST")


    def do_GET(self):
        print("test")
        self.send_response(200)
        self.end_headers()
        with urllib.request.urlopen(self.path[1:]) as url:
            shutil.copyfileobj(url, self.wfile)

port = 4443
host = 'localhost'
sslctx = ssl.SSLContext()
sslctx.check_hostname = False # If set to True, only the hostname that matches the certificate will be accepted
sslctx.load_cert_chain(keyfile='./key.pem', certfile="./cert.pem")

httpd = HTTPServer((host, port), Test)
httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)

print(f"Server running on {host}:{port}")

httpd.serve_forever()
