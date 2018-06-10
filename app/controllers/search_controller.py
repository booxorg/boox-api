import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import liteframework.validator as Validator

import app.models.book as Book
import app.models.author_book as AuthorBook
import app.middleware.token_valid as TokenCheck
import book_controller as BookController
import MySQLdb
from datetime import datetime

@Routing.Route(
    url='/search',
    method='GET',
    middleware=[
        TokenCheck.token_valid, 
        Params.has_params('token', 'keywords')
    ]
)
def search(variables={}, request={}):
    keywords = request.params['keywords']
    authors = request.params.get('authors', '.*')
    genres = request.params.get('genres', '.*')
    before = request.params.get('before', '-')
    after = request.params.get('after', '-')
    location = request.params.get('location', '-')

    ok, error_message = Validator.validate([
        (keywords, r'^[a-zA-Z0-9, \'"+-=;?]+$', 'keywords value is invalid'),
        (authors, r'^\.\*|[\w\'-, ]+$', 'authors value is invalid'),
        (genres, r'^\.\*|(%s)$' % ('|'.join(BookController.genres)), 'genres value is invalid'),
        (before, r'^\-|([1-9]|([012][0-9])|(3[01]))\-([0]{0,1}[1-9]|1[012])\-\d\d\d\d$', 'before value is invalid'),
        (after, r'^\-|([1-9]|([012][0-9])|(3[01]))\-([0]{0,1}[1-9]|1[012])\-\d\d\d\d$', 'after value is invalid'),
    ])

    result = []
    try:
        if not ok:
            raise UserWarning(error_message)
        search_results = Book.Book().query('BOOKS.ID', 'BOOKS.ISBN', 'BOOKS.TITLE', 'BOOKS.GENRE', 'BOOKS.EXPIRES', 'BOOKS.AUTHORID', 'AUTHORS.NAME')\
            .join('AUTHORS', 'AUTHORID', 'ID')\
            .where('BOOKS.title', 'REGEXP', '|'.join(keywords.split(',')))\
            .condition('AND', 'BOOKS.GENRE', 'REGEXP', '|'.join(genres.split(',')))\
            .condition('AND', 'AUTHORS.NAME', 'REGEXP', '|'.join(authors.split(',')))

        if before != '-':
            before = datetime.strptime(before, '%d-%m-%Y').strftime('%Y-%m-%d')
            search_results = search_results.condition('AND', 'BOOKS.EXPIRES', '<', before)
        if after != '-':
            after = datetime.strptime(after, '%d-%m-%Y').strftime('%Y-%m-%d')
            search_results = search_results.condition('AND', 'BOOKS.EXPIRES', '>', after)
        search_results = search_results.get()
            
        for search_result in search_results:
            book = {}
            book['title'] = search_result['BOOKS.TITLE'].decode('cp1252')
            book['id'] = search_result['BOOKS.ID']
            book['isbn'] = search_result['BOOKS.ISBN']
            book['genre'] = search_result['BOOKS.GENRE']
            book['expires'] = search_result['BOOKS.EXPIRES'].strftime('%d-%m-%Y')
            book['author'] = search_result['AUTHORS.NAME'].decode('cp1252')
            result.append(book)

    except UserWarning, e:
        print 'user warining: ', repr(e)
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

