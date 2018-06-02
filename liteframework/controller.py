import magic
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from liteframework.application import Application

class Controller(object):

    @staticmethod
    def response():
        response = 'hello, user'
        return (
            {
                'Content-type' : 'text/plain',
                'Content-Length' : str(len(response))
            },
            response.encode('utf-8'),
            '200 OK'
        )

    # Should return dictionary with response headers as key and value
    @staticmethod
    def resource(resource_data, resource_mimetype=None):
        if resource_mimetype == None:
            resource_mimetype = magic.from_buffer(resource_data, mime = True)

        return (
            {
                'Content-type' : resource_mimetype,
                'Content-Length' : str(len(resource_data))
            },
            resource_data.encode('utf-8'),
            '200 OK'
        )

    @staticmethod
    def response_file(resource_url, resource_mimetype=None):
        if resource_mimetype == None:
            resource_mimetype = magic.from_file(resource_url, mime = True)
        
        try:
            with open(resource_url, 'rb') as f:
                resource_data = f.read()
        except:
            resource_data = ''

        return (
            {
                'Content-type' : resource_mimetype,
                'Content-Length' : str(len(resource_data))
            },
            resource_data.encode('utf-8'),
            '200 OK'
        )

    @staticmethod
    def response_not_found():
        response = '404, Not Found, Sowy'
        return (
            {
                'Content-type' : 'text/plain',
                'Content-Length' : str(len(response))
            },
            response.encode('utf-8'),
            '404 Not Found'
        )

    @staticmethod
    def view(name, pass_variables = {}):
        template = Application.jinja_env.get_template('common.html')
        response = template.render(page_name='main.html')
        return (
            {
                'Content-type' : 'text/html',
                'Content-Length' : str(len(response))
            },
            response.encode('utf-8'),
            '200 OK'
        )


