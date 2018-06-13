import liteframework.application as App
import liteframework.controller as Controller 
import liteframework.routing as Routing 

import app.models.user as User
import app.models.book as Book
import app.models.user_book as UserBook
import app.models.location as Location
import app.models.exchange as Exchange
import app.models.author as Author
import logging

@Routing.Route(
    url='/report/info', 
    method='GET'
)
def general_info(variables={}, request={}):
    users = 0
    connections = 0
    locations = 0
    books = 0
    authors = 0
    nearby = 0
    try:
        users = User.User().count().get()[0]['count']
        connections = Exchange.Exchange().count().get()[0]['count']
        locations = Location.Location().count().get()[0]['count']
        books = Book.Book().count().get()[0]['count']
        authors = Author.Author().count().get()[0]['count']
        nearby = 0
    except Exception, e:
        print str(e)
        pass

    return Controller.response_json({
        'status' : 'success',
        'message' : 'statistics collected',
        'response' : {
            'users' : users,
            'connections' : connections,
            'locations' : locations,
            'books' : books,
            'authors' : authors,
            'nearby' : nearby
        }    
    })