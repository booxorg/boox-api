import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import liteframework.validator as Validator
import app.models.book as Book
import app.models.user_book as UserBook
import app.models.author as Author
import urllib2
import xmltodict
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
    key = App.config.get('GOODREADS', 'key')
    query = request.params['query']
    limit = request.params.get('limit', '')

    goodreads_api = 'https://www.goodreads.com/search/index.xml?key={}&q={}&search[title]'.format(key, query)
    api_response = urllib2.urlopen(goodreads_api)
    api_response_data = api_response.read().decode(api_response.headers.getparam("charset"))
    api_dict = dict()

    result = {}
    try:
        api_dict = xmltodict.parse(api_response_data)
        api_work = api_dict['GoodreadsResponse']['search']['results']['work']
        result['books'] = []
        for api_book in api_work:
            try:
                book = {}
                book['goodreads_id'] = int(api_book['best_book']['id']['#text'])
                book['title'] = api_book['best_book']['title']
                book['author'] = api_book['best_book']['author']['name']
                book['author_id'] = api_book['best_book']['author']['id']['#text']
                book['image_url'] = api_book['best_book']['image_url']
                book['small_image_url'] = api_book['best_book']['small_image_url']
                if 'original_publication_day' in api_book and 'original_publication_month' in api_book:
                    book['publication_date'] = '{}-{}-{}'.format(
                        api_book['original_publication_day']['#text'], 
                        api_book['original_publication_month']['#text'], 
                        api_book['original_publication_year']['#text']
                    )
                else:
                    book['publication_date'] = api_book['original_publication_year']['#text']
                result['books'].append(book)
            except:
                pass
    except Exception, e:
        print str(e)
    return Controller.response_json(result)


@Routing.Route(
    url='/book/create', 
    method='GET', 
    middleware=[
        TokenCheck.token_valid, 
        Params.has_params('token', 'title', 'author', 'expires', 'genre')
    ]
)
def add_book(variables={}, request={}):
    status = 'success'
    message = ''
    values = None

    title = request.params['title']
    author = request.params['author']
    expires = request.params['expires']
    genre = request.params['genre']
    ok, error_message = Validator.validate([
        (title, r'[A-Za-z0-9\s\-_,\.;:()]+', 'title value is invalid'),
        (author, r'[a-zA-Z0-9 ,.\'-]+', 'author value is invalid'),
        (genre, r'(%s)' % ('|'.join(genres)), 'genre value is invalid'),
        (expires, r'([1-9]|([012][0-9])|(3[01]))\-([0]{0,1}[1-9]|1[012])\-\d\d\d\d', 'expires value is invalid')
    ])

    if not ok:
        status = 'error',
        message = error_message
    else:
        datetime_object = datetime.strptime(expires, '%d-%m-%Y')
        craeted_book = Book.Book().insert({
            'ISBN' : '0123456789876',
            'title' : title,
            'genre' : genre,
            'expires' : datetime_object.strftime('%Y-%m-%d')
        })

        created_author = Author.Author().update_or_create({'NAME' : author}, {'NAME' : author})

    result = {
        'status' : status,
        'message' : message,
        'response' : values
    }
    return Controller.response_json(result)
