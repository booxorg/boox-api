class Router(object):
    routing_table = {}

    @staticmethod
    def route_url(url):
        print url
        if url in Router.routing_table:
            action_function = Router.routing_table[url]
            return action_function([])
        else:
            return 'Failed'


def route(*args, **kwargs):
    def decorator(action_method):
        def wrapper(*args1, **kwargs1):
            result = action_method(*args1, **kwargs1)
            return result
        Router.routing_table[kwargs['url']] = action_method   
        return wrapper
    return decorator

