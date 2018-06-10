import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import liteframework.validator as Validator

import app.models.book as Book
import app.models.user_book as UserBook
import app.models.author_book as AuthorBook
import app.models.author as Author
import app.models.token as Token
import app.api.goodreads_api as Goodreads
import MySQLdb
from datetime import datetime

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

@Routing.Route(url='/search-title', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token','query')])
def search_external(variables={}, request={}):
    query = request.params['query']
    limit = request.params.get('limit', '0')

    ok, error_message = Validator.validate([
        (query, r'^[a-zA-Z0-9, \'"+-=;?]+$', 'title query is invalid'),
        (limit, r'^([0-9]|[1-9][0-9]+)$', 'limit value is invalid, should be a positive number')
    ])

    try:
        if not ok:
            raise UserWarning(error_message)

        limit = int(limit)
        result = Goodreads.request_search(query, limit)

    except UserWarning, e:
        print 'user warining: ', str(e)
        return Controller.response_json({
            'status' :  'error',
            'message' : str(e)   
        })
    except Exception, e:
        print 'fatal error: ', repr(e)
        return Controller.response_json({
            'status' :  'error',
            'message' : 'fatal error occured'   
        })

    return Controller.response_json({
        'status' : 'success',
        'message' : 'search sucessful',
        'response' : result    
    })


@Routing.Route(
    url='/book/create', 
    method='GET', 
    middleware=[
        TokenCheck.token_valid, 
        Params.has_params('token', 'expires', 'genre', 'goodreads_id')
    ]
)
def add_book(variables={}, request={}):
    status = 'success'
    message = ''
    values = {}

    #title = request.params['title']
    #author = request.params['author']
    expires = request.params['expires']
    genre = request.params['genre']
    goodreads_id = request.params['goodreads_id']
    ok, error_message = Validator.validate([
        #(title, r'^[A-Za-z0-9\s\-_,\.;:()]+$', 'title value is invalid'),
        #(author, r'^[a-zA-Z0-9 ,.\'-]+$', 'author value is invalid'),
        (genre, r'^(%s)$' % ('|'.join(genres)), 'genre value is invalid'),
        (expires, r'^([1-9]|([012][0-9])|(3[01]))\-([0]{0,1}[1-9]|1[012])\-\d\d\d\d$', 'expires value is invalid'),
        (goodreads_id, r'^[0-9]|[1-9][0-9]+$', 'goodreads_id value is invalid')
    ])

    try:
        if not ok:
            raise UserWarning(error_message)
        book = Goodreads.find_book_by_id(int(goodreads_id))
        if not book:
            raise UserWarning('no book with such id was found')

        current_user_id = Token.Token().query('USERID').where('TOKEN', '=', request.params['token']).get()[0]['USERID']
        if not current_user_id or current_user_id == 0:
            raise UserWarning('invalid user connected to token')

        created_author = Author.Author().update_or_create({'NAME' : book['author']}, {'NAME' : book['author']})
        if not created_author:
            raise UserWarning('unable to create or update the book author')

        
        datetime_object = datetime.strptime(expires, '%d-%m-%Y')
        created_book = Book.Book().insert({
            'ISBN' : book['isbn'],
            'TITLE' : book['title'],
            'GENRE' : genre,
            'EXPIRES' : datetime_object.strftime('%Y-%m-%d'),
            'AUTHORID' : created_author['ID']
        })
        if not created_book:
            raise UserWarning('unable to add book to the database')

        created_user_book = UserBook.UserBook().insert({
            'BOOKID' : created_book['ID'],
            'USERID' : current_user_id   
        })
        if not created_user_book:
            raise UserWarning('unable to connect user to book')

        message = 'the book has been added'
        values['book_id'] = created_book['ID']
        values['user_id'] = current_user_id
        values['author_id'] = created_author['ID']
        
    except UserWarning, e:
        print 'User Warning: ', str(e)
        return Controller.response_json({
            'status' : 'error',
            'message' : str(e)    
        })
    except (MySQLdb.Error, MySQLdb.Warning), e:
        print 'DB exception: ', str(e)
        return Controller.response_json({
            'status' : 'error',
            'message' : 'there are problems connecting to server database'  
        })
    except Exception, e:
        print 'Fatal exception: ', str(e)
        return Controller.response_json({
            'status' : 'error',
            'message' : 'fatal error occured'  
        })

    return Controller.response_json({
        'status' : status,
        'message' : message,
        'response' : values
    })
