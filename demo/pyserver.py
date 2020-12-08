#!/usr/bin/env python3
import sys
sys.path.append('..')

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

from emrap.utils import randstr

class Server(BaseHTTPRequestHandler):
    @property
    def full(self):
        return '{}\r\n{}\r\n{}'.format(
            self.requestline, self.headers, self.body.decode('utf-8'))

    def send_full_response(self):
        data = 'token: {}'.format(randstr(16))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Set-Cookie', 'Foo={}'.format(randstr(10)))
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

    def _show(self):
        logging.info('''
----- Request Start ----->

{}

<----- Request End -----
'''.format(self.full))

    def do_GET(self):
        content_length = int(self.headers.get('Content-Length', 0))
        self.body = self.rfile.read(content_length)
        self._show()
        self.send_full_response()

    def do_POST(self):
        self.do_GET()

    def do_PUT(self):
        self.do_GET()

    def do_DELETE(self):
        self.do_GET()

def run():
    logging.basicConfig(level=logging.INFO)
    port = 50001
    httpd = HTTPServer(('localhost', port), Server)
    logging.info(
        'Starting httpd on http://localhost:{}'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopped httpd')


if __name__ == '__main__':
    run()
