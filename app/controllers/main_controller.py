import liteframework.controller as Controller 
import liteframework.routing as Routing 

@Routing.Route(url='/', method='GET')
def index(variables={}, request={}):
    pass_variables = {'name' : 'liteframework'}
    return Controller.response_view('default.html', pass_variables)