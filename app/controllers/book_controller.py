import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import json

@Routing.Route(url='/book/{book_id::\d+}', method='GET', middleware=[Params.has_params('token')])
def get_book(variables={}, request={}):
    status = 'success'
    message = ''
    values = None

    if not 'token' in request.params:
        status = 'error'
        message = 'not authorized'
    else:
        message = 'book returned'
        values = {
            'token' : request.params['token'],
            'book_id' : variables['book_id']
        }

    result = {
        'status' : status,
        'message' : message,
        'result' : values
    }
    return Controller.response_json(result)
