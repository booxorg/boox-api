import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.middleware.params as Params
import liteframework.validator as Validator

import app.models.user as User
import app.models.book as Book
import app.models.user_book as UserBook
import app.models.location as Location
import app.models.exchange as Exchange
import app.models.token as Token
import MySQLdb
from datetime import datetime
import logging

@Routing.Route(
    url='/user', 
    method='GET',
    middleware=[
        Params.has_params('id')
    ]
)
def user_info(variables={}, request={}):
    id = request.params['id']

    ok, error_message = Validator.validate([
        (id, r'^[0-9]|[1-9][0-9]+$', 'id value is invalid')
    ])
    user = {}
    try:
        if not ok:
            raise UserWaning(error_message)
        found_user = User.User().query('*').where('ID', '=', id).get()
        if not found_user:
            raise UserWarning('no such user')
        found_user = found_user[0]
        book_count = UserBook.UserBook().count().where('USERID', '=', found_user['ID']).get()[0]
        user = {
            'id' : found_user['ID'],
            'username' : found_user['USERNAME'],
            'first_name' : found_user['FIRSTNAME'],
            'last_name' : found_user['LASTNAME'],
            'email' : found_user['EMAIL'],
            'book_count' : book_count['count']
        }

    except UserWarning, e:
        logging.exception('User warning')
        return Controller.response_json({
            'status' :  'error',
            'message' : str(e)   
        })
    except Exception, e:
        logging.exception('Fatal error')
        return Controller.response_json({
            'status' :  'error',
            'message' : 'fatal error occured'   
        })

    return Controller.response_json({
        'status' : 'success',
        'message' : 'search sucessful',
        'response' : user    
    })