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
        books_query = Book.Book()\
            .query('BOOKS.ID', 'BOOKS.ISBN', 'BOOKS.TITLE', 'BOOKS.GENRE', 
            'BOOKS.EXPIRES', 'BOOKS.AUTHORID', 'BOOKS.COVER', 'BOOKS.DELETED', 'AUTHORS.NAME')\
            .join('AUTHORS', 'AUTHORID', 'ID')\
            .join('USERBOOKS', 'ID', 'BOOKID')\
            .where('USERBOOKS.USERID', '=', found_user['ID']).get()

        books = []
        for book_result in books_query:
            book = {}
            book['user_id'] = found_user['ID']
            book['username'] = found_user['USERNAME']
            book['title'] = book_result['BOOKS.TITLE'].decode('cp1252')
            book['id'] = book_result['BOOKS.ID']
            book['isbn'] = book_result['BOOKS.ISBN'].decode('cp1252')
            book['genre'] = book_result['BOOKS.GENRE'].decode('cp1252')
            book['expires'] = book_result['BOOKS.EXPIRES'].strftime('%d-%m-%Y')
            book['author'] = book_result['AUTHORS.NAME'].decode('cp1252')
            if book_result['BOOKS.COVER']:
                book['cover'] = book_result['BOOKS.COVER'].decode('cp1252')
            else:
                book['cover'] = ''
            books.append(book)
        user = {
            'id' : found_user['ID'],
            'username' : found_user['USERNAME'],
            'first_name' : found_user['FIRSTNAME'],
            'last_name' : found_user['LASTNAME'],
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