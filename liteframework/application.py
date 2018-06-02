####################################################################################
####
####    This static class holds the main information about the paths and environmental 
####    variables. 
####    It gets instantiated at the very start of the request, in the public/index.wsgi
####    To use paths, env and start_response function - import this class
####    from liteframework.application import Application
####    and access members statically
####    Application.public_path, Application.jinja_env
####
####################################################################################
import os, sys
from liteframework.util import url_reconstruction
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

class Application(object):
    environ = None
    start_response = None
    base_path = None 
    public_path = None
    app_path = None
    resources_path = None
    views_path = None
    jinja_env = None

    @staticmethod
    def init(environ, start_response, base_path):
        Application.environ = environ
        Application.start_response = start_response
        Application.request_url = url_reconstruction(environ)
        Application.base_path = os.path.realpath(base_path)
        Application.public_path = os.path.join(Application.base_path, 'public')
        Application.resources_path = os.path.join(Application.base_path, 'resources')
        Application.views_path = os.path.join(Application.base_path, 'resources', 'views')
        Application.app_path = os.path.join(Application.base_path, 'app')
        Application.jinja_env = Environment(
            loader=FileSystemLoader(Application.views_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

