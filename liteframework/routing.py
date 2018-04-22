from liteframework.util import match_url

class Router(object):
    routing_table = {}

    @staticmethod
    def route_url(url):
        for key, action in Router.routing_table.iteritems():
            result, variables = match_url(key, url)
            if result:
                print 'url {} matched route {}, variables={}'.format(url, key, variables)
                return action(variables)
        return 'Failed'


def route(*args, **kwargs):
    def decorator(action_method):
        def wrapper(*args1, **kwargs1):
            result = action_method(*args1, **kwargs1)
            return result
        Router.routing_table[kwargs['url']] = action_method   
        return wrapper
    return decorator

