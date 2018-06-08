import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import json

@Routing.Route(url='/book/{book_id::\d+}', method='GET')
def get_book(variables={}, request={}):
    result = {
        'status' : 'Success',
        'book_id' : variables['book_id'],
        'limit' : variables['limit']
    }
    return Controller.response_data(json.dumps(result), response_mimetype='text/json')
