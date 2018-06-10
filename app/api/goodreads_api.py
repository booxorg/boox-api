import urllib2
import xmltodict
from datetime import datetime
import liteframework.application as App

def work_xml_adaptor(api_work, limit):
    books = []
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
            books.append(book)
        except:
            pass
    if limit != 0:
        del books[limit:]
    return books    


def book_xml_adaptor(api_book):
    book = {}
    try:
        book['goodreads_id'] = int(api_book['id'])
        book['title'] = api_book['title']
        book['isbn'] = api_book['isbn']
        book['image_url'] = api_book['image_url']
        book['small_image_url'] = api_book['small_image_url']
        book['publication_date'] = '{}-{}-{}'.format(
            api_book['publication_day'], 
            api_book['publication_month'], 
            api_book['publication_year']
        )
        book['author'] = api_book['authors']['author'][0]['name']
    except:
        return dict()
    return book

def request_search(query, limit):
    key = App.config.get('GOODREADS', 'key')
    goodreads_api = 'https://www.goodreads.com/search/index.xml?key={}&q={}&search[title]'.format(key, query)
    api_response = urllib2.urlopen(goodreads_api)
    if not api_response:
        raise UserWarning('unable to request goodreads api')
    api_response_data = api_response.read().decode(api_response.headers.getparam("charset"))
    if not api_response_data:
        raise UserWarning('nothing found')

    api_dict = dict()
    result = []
    try:
        api_dict = xmltodict.parse(api_response_data)
        api_work = api_dict['GoodreadsResponse']['search']['results']['work']
        result = work_xml_adaptor(api_work, limit)
    except (xmltodict.ParsingInterrupted, ValueError), e:
        raise UserWarning('unable to parse goodreads xml')
    return result


def find_book_by_id(id):
    key = App.config.get('GOODREADS', 'key')
    goodreads_api = 'https://www.goodreads.com/book/show?key={}&id={}'.format(key, id)
    api_response = urllib2.urlopen(goodreads_api)
    if not api_response:
        raise UserWarning('unable to request goodreads api')
    api_response_data = api_response.read().decode(api_response.headers.getparam("charset"))
    if not api_response_data:
        raise UserWarning('nothing found')

    api_dict = dict()
    book = None
    try:
        api_dict = xmltodict.parse(api_response_data)
        if not 'GoodreadsResponse' in api_dict or \
           not 'book' in api_dict['GoodreadsResponse']:
           raise UserWarning('No dictionary keys')
        api_book = api_dict['GoodreadsResponse']['book']
        book = book_xml_adaptor(api_book)
    except (xmltodict.ParsingInterrupted, ValueError), e:
        raise UserWarning('unable to parse goodreads xml')
    return book