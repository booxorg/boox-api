import liteframework.controller as Controller
import json

def has_params(*params):
    def closure(variables={}, request={}):
        for param in params:
            if not param in request.params: 
                result = {
                    'status' : 'failed',
                    'message' : 'Parameter %s should be present' % (param)
                }
                return (False, Controller.response_json(result))
        return (True, None)
    return closure