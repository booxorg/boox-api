import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import liteframework.validator as Validator

import app.models.user as User
import app.models.book as Book
import app.models.user_book as UserBook
import app.models.location as Location
import app.models.exchange as Exchange
import app.models.token as Token
import book_controller as BookController
import MySQLdb
from datetime import datetime
import logging
import bcrypt

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
        books_query = Book.Book()\
            .query('BOOKS.ID')\
            .join('USERBOOKS', 'ID', 'BOOKID')\
            .where('USERBOOKS.USERID', '=', found_user['ID']).get()

        books = []
        for book_result in books_query:
            book = BookController.get_book_by_id(book_result['BOOKS.ID'])
            books.append(book)

        location = Location.Location().query('*').where('USERID', '=', found_user['ID']).get()
        if location:
            location = location[0]
        else:
            location = dict()

        user = {
            'id' : found_user['ID'],
            'username' : found_user['USERNAME'],
            'first_name' : found_user['FIRSTNAME'],
            'last_name' : found_user['LASTNAME'],
            'country' : location.get('COUNTRY', ''),
            'city' : location.get('CITY', ''),
            'street' : location.get('STREET', ''),
            'email' : found_user['EMAIL'],
            'book_count' : book_count['count'],
            'books' : books
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

###############################################################################################################
@Routing.Route(url='/user/info', method = 'GET', middleware=[TokenCheck.token_valid, Params.has_params('token')])
def user_info(variables={}, request={}):

    result = {}
    try:
        user_id = Token.Token().query('USERID').where('TOKEN', '=', request.params['token']).get()[0]['USERID']
        user_query = User.User()\
            .query('USERS.ID', 'USERS.USERNAME', 'USERS.FIRSTNAME', 'USERS.LASTNAME', 'USERS.EMAIL')\
            .where('USERS.ID', '=', user_id).get()[0]
        locations = Location.Location()\
            .query('LOCATIONS.COUNTRY', 'LOCATIONS.CITY', 'LOCATIONS.STREET')\
            .where('USERID', '=', user_id).get()
        if locations:
            locations = locations[0]
        else:
            locations = dict()


        result['firstname'] = user_query['USERS.FIRSTNAME']
        result['lastname'] = user_query['USERS.LASTNAME']
        result['email'] = user_query['USERS.EMAIL']
        result['country'] = locations.get('LOCATIONS.COUNTRY', '')
        result['city'] = locations.get('LOCATIONS.CITY', '')
        result['street'] = locations.get('LOCATIONS.STREET', '')

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
        'message' : 'edit sucessful',
        'response' : result    
    })


###############################################################################################################
@Routing.Route(url='/user/edit', method = 'GET', middleware=[TokenCheck.token_valid, Params.has_params('token')])
def user_edit(variables={}, request={}):
    status = 'success'
    message = ''

    fname = request.params.get('fname', '')
    lname = request.params.get('lname', '')
    email = request.params.get('email', '')       
    password = request.params.get('password', None)
    new_password = request.params.get('npassword', None)
    confirm_new_password = request.params.get('cnpassword', None)
    country = request.params.get('country', '')
    city = request.params.get('city', '')
    street = request.params.get('street', '')

    result = None
    try:
        if not fname or not lname or not email:
            raise UserWarning('firstname, lastname and email are mandatory fields')
        user_id = Token.Token().query('USERID').where('TOKEN', '=', request.params['token']).get()[0]['USERID']

        User.User().update({'FIRSTNAME' : fname, 'LASTNAME' : lname, 'EMAIL' : email}).where('ID', '=', user_id).execute()
        user = User.User().query('*').where('ID', '=', user_id).get()[0]

        if country or city or street:
            Location.Location().update_or_create(
                {
                'USERID' : user_id    
                }, 
                {
                    'USERID' : user_id,
                    'COUNTRY' : country,
                    'CITY' : city,
                    'STREET' : street
                }
            )

        if password:
            old_password_hash = bcrypt.hashpw(password.encode('utf8'), user['SALT'])
            if old_password_hash != user['PASSWORD']:
                raise UserWarning('password incorrect')
            if new_password != confirm_new_password:
                raise UserWarning('new password and confirm password don\'t match')
            else:
                new_password_hash = bcrypt.hashpw(new_password.encode('utf8'), user['SALT'])
                User.User().update({'PASSWORD' : new_password_hash}).where('ID', '=', user_id).execute()

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
        'message' : 'edit sucessful',
        'response' : result    
    })

    