import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import json

@Routing.Route(url='/register/form', method = 'GET')
def register(variables={}, request={}):
    
    return Controller.response_view('form.html')
    