from liteframework.util import match_url
from liteframework.application import Application
from liteframework.controller import Controller

class Router(object):
    routing_table = {}

    @staticmethod
    def route_url(url):
        print 'url: ', url
        for key, action in Router.routing_table.iteritems():
            result, variables = match_url(key, url)
            if result:
                print 'url {} matched route {}, variables={}'.format(url, key, variables)
                return action(variables)
        return Controller.response_not_found()

    @staticmethod
    def handle_request():
        output, content, status = Router.route_url(Application.request_url)
        response_headers = output.items()
        Application.start_response(status, response_headers)
        return content


def Route(*args, **kwargs):
    def decorator(action_method):
        def wrapper(*args1, **kwargs1):
            result = action_method(*args1, **kwargs1)
            return result
        Router.routing_table[kwargs['url']] = action_method   
        return wrapper
    return decorator

