import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import json

genres = [
    'Comedy',
    'Drama',
    'Romance',
    'SciFi',
    'Cooking'
]

@Routing.Route(url='/genres', method='GET')
def get_genres(variables={}, request={}):
    global genres
    result = {
        'status' : 'success',
        'message' : 'genres',
        'response' : {
            'genres' : genres
        }
    }
    return Controller.response_json(result)

@Routing.Route(url='/book/create', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token')])
def get_book(variables={}, request={}):
    status = 'success'
    message = ''
    values = None

    result = {
        'status' : status,
        'message' : message,
        'response' : values
    }
    return Controller.response_json(result)
