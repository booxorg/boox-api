import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import liteframework.validator as Validator
import app.models.book as Book
import app.models.user_book as UserBook
import app.models.author as Author

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


@Routing.Route(
    url='/book/create', 
    method='GET', 
    middleware=[
        TokenCheck.token_valid, 
        Params.has_params('token', 'title', 'authors', 'expires', 'genre')
    ]
)
def get_book(variables={}, request={}):
    status = 'success'
    message = ''
    values = None

    title = request.params['title']
    authors = request.params['authors']
    expires = request.params['expires']
    genre = request.params['genre']
    ok, error_message = Validator.validate([
        (title, r'[A-Za-z0-9\s\-_,\.;:()]+', 'title value is invalid'),
        (authors, r'[a-zA-Z0-9 ,.\'-]+', 'authods value is invalid'),
        (genre, r'(%s)' % ('|'.join(genres)), 'genre value is invalid'),
        (expires, r'([1-9]|([012][0-9])|(3[01]))\-([0]{0,1}[1-9]|1[012])\-\d\d\d\d\s([0-1]?[0-9]|2?[0-3]):([0-5]\d)', 'expires value is invalid')
    ])

    if not ok:
        status = 'error',
        message = error_message
    else:
        Book.Book().insert({
            'ISBN' : '0123456789876',
            'title' : title,
            'genre' : genre,
            'expires' : expires
        })

        authors_array = authors.strip().split()
        for author_name in authors_array:
            created_author = Author.Author().update_or_create({'NAME' : author_name}, {'NAME' : author_name})

    result = {
        'status' : status,
        'message' : message,
        'response' : values
    }
    return Controller.response_json(result)
