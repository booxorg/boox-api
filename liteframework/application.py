import os, sys
from app.routes import *
from liteframework.routing import Router
from liteframework.util import url_reconstruction

class Application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.request_url = url_reconstruction(environ)

    def handle_request(self):
        status = '200 OK'
        output = Router.route_url(self.request_url)
        

        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(output)))]
        self.start_response(status, response_headers)
        return [output]
