import liteframework.util as Util
import liteframework.application as App
import liteframework.controller as Controller
import copy


class RouteObject:
    def __init__(self):
        self.template = None
        self.action = None
        self.method = None
        self.middleware = None

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
            App.routing_table[kwargs['url']] = copy.deepcopy(new_route)

        return wrapper
    return decorator


def route_url(request):
    for template, route in App.routing_table.iteritems():
        if request.method == route.method:
            result, variables = Util.match_url(template, request.url)
            if result:
                print 'url {} matched route {}, variables={}'.format(request.url, template, variables)
                return route.action(request=request, variables=variables)
    return Controller.response_not_found()

def handle_request(request):
    output, content, status = route_url(request)
    response_headers = output.items()
    App.start_response(status, response_headers)
    return content




