#!/usr/bin/python2.7
import sys, os
import monitor
import posixpath
monitor.start(interval=1.0)
monitor.track(os.path.join(os.path.dirname(__file__), '..'))

import liteframework.application as App
import liteframework.util as Util
import liteframework.routing as Routing
import liteframework.post as Post
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

# Import user defined routes
from app.controllers import *

# Import all the default global functions
from liteframework.global_functions import *

#####################################################################################
###    The entry point of the application. 
###    Apache offsers control by calling this function and regains control after it finishes
#####################################################################################

def application(environ, start_response):   
    # Wrapper to set SCRIPT_NAME to actual mount point.
    environ['SCRIPT_NAME'] = posixpath.dirname(environ['SCRIPT_NAME'])
    if environ['SCRIPT_NAME'] == '/':
        environ['SCRIPT_NAME'] = ''
    path = os.path.join(os.path.dirname(__file__), '..')

    # Globals init start
    App.environ = environ
    App.start_response = start_response
    App.request_url = Util.url_reconstruction(environ)
    App.base_path = os.path.realpath(path)
    App.public_path = os.path.join(App.base_path, 'public')
    App.resources_path = os.path.join(App.base_path, 'resources')
    App.views_path = os.path.join(App.base_path, 'resources', 'views')
    App.app_path = os.path.join(App.base_path, 'app')
    App.jinja_env = Environment(
        loader=FileSystemLoader(App.views_path),
        autoescape=select_autoescape(['html', 'xml'])
    )
    App.jinja_env.globals.update(**App.global_functions)
    # Globals init finish

    
    # Request build
    request = Routing.Request()
    request.port = environ.get('SERVER_PORT', 80)
    request.method = environ.get('REQUEST_METHOD', 'GET')
    request.protocol = environ.get('SERVER_PROTOCOL', 'http')
    request.content_length = environ.get('CONTENT_LENGTH', 0)
    request.user_agent = environ.get('HTTP_USER_AGENT', '')
    request.request_scheme = environ.get('REQUEST_SCHEME', 'http')
    request.remote_port = environ.get('REMOTE_PORT', 0)
    request.lang = environ.get('HTTP_ACCEPT_LANGUAGE', 'en')
    request.content_type = environ.get('CONTENT_TYPE', 'text/html')
    request.accept_encoding = environ.get('HTTP_ACCEPT_ENCODING', 'compress')
    request.input = Post.get_post_form(environ)
    request.url = App.request_url
    # Request build finish

    # Load user defined routes


    return Routing.handle_request(request)

