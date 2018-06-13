import liteframework.util as Util
import liteframework.application as App
import liteframework.controller as Controller
import copy
import logging


class RouteObject:
    def __init__(self):
        self.template = None
        self.action = None
        self.method = None
        self.middleware = None
        self.disabled = False

class Request:
    def __init__(self):
        self.port = None
        self.protocol = None
        self.content_length = None
        self.user_agent = None
        self.request_scheme = None
        self.remote_port = None
        self.lang = None
        self.content_type = None
        self.accept_encoding = None
        self.method = None
        self.url = None
        self.input = None    
        self.cookies = None
        self.new_cookies = None
        self.params = None
        self.url_no_params = None

    def get(self, key, default):
        pass

def Route(*args, **kwargs):
    def decorator(action_method):
        def wrapper(*args1, **kwargs1):
            result = action_method(*args1, **kwargs1)
            return result
        if kwargs['url']:    
            new_route = RouteObject()
            new_route.template = kwargs['url']
            new_route.method = 'GET' if 'method' not in kwargs else kwargs['method']
            new_route.action = action_method
            new_route.disabled = False if 'disabled' not in kwargs else kwargs['disabled']
            new_route.middleware = [] if 'middleware' not in kwargs else kwargs['middleware']
            if not new_route.disabled:
                App.routing_table.append(new_route)
        return wrapper
    return decorator


def route_url(request):
    for route in App.routing_table:
        if request.method == route.method and route.disabled == False:
            result, variables = Util.match_url(route.template, request.url_no_params)
            if result:
                for middleware_func in route.middleware:
                    result, return_value = middleware_func(variables, request)
                    if not result:
                        return return_value

                print 'url {} matched route {}, variables={}'.format(request.url, route.template, variables)
                return route.action(request=request, variables=variables)
    return Controller.response_not_found()

def handle_request(request):
    try:
        output, content, status = route_url(request)
    except Exception, e:
        logging.exception('Failed to execute request')
        raise   
    response_headers = output.items()
    response_headers.append(('Cache-Control', 'no-store'))
    response_headers.append(('Access-Control-Allow-Origin', '*'))
    for cookie in request.new_cookies.values():
        response_headers.append(('Set-Cookie', cookie.OutputString()))
    App.start_response(status, response_headers)
    return content




