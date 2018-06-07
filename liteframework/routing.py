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
            if not new_route.disabled:
                App.routing_table[kwargs['url']] = copy.deepcopy(new_route)
        return wrapper
    return decorator


def route_url(request):
    for template, route in App.routing_table.iteritems():
        if request.method == route.method and route.disabled == False:
            result, variables = Util.match_url(template, request.url_no_params)
            if result:
                print 'url {} matched route {}, variables={}'.format(request.url, template, variables)
                if request.params:
                    for (key, value) in request.params.items():
                        variables.update({key: value[0]})
                return route.action(request=request, variables=variables)
    return Controller.response_not_found()

def handle_request(request):
    output, content, status = route_url(request)
    response_headers = output.items()

    for cookie in request.new_cookies.values():
        response_headers.append(('Set-Cookie', cookie.OutputString()))
    App.start_response(status, response_headers)
    return content




