import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import app.models.token as Token
import app.models.user_book as UserBook
import app.models.exchange as Exchange
import app.models.book as Book
import datetime

@Routing.Route(url='/exchange/propose', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'bookid')])
def propose_exchange(variables={}, request={}):
	status = 'success'
	message = ''

	token = request.params['token']
	book_id = request.params['bookid']
	
	dict_book = Book.Book().query("DELETED").where("ID", "=", book_id).get()
	if not dict_book:
		status = 'error'
		message = 'the book does not exist'
	elif (dict_book[0]['DELETED'] == 1):
		status = 'error'
		message = 'the book is not available for exchange'
	else:
		dict_receiver = Token.Token().query("USERID").where("TOKEN", "=", token).get()
		dict_owner = UserBook.UserBook().query("USERID").where("BOOKID", "=", book_id).get()

		if(dict_receiver[0]['USERID'] == dict_owner[0]['USERID']):
			status = 'error'
			message = 'users cannot send requests to themselves'
		else:
			dict_exchange = Exchange.Exchange().query('ID').where("OWNERID", "=", dict_owner[0]['USERID']). \
							condition("AND", "RECEIVERID", "=", dict_receiver[0]['USERID']). \
							condition("AND", "BOOKID", "=", book_id).get()
			if(dict_exchange):
				status = 'error'
				message = 'the exchange already exists'
			else:
				date = datetime.datetime.now().strftime("%Y-%m-%d")

				insert_dict = { 
								'OWNERID' : dict_owner[0]['USERID'], 'RECEIVERID' : dict_receiver[0]['USERID'],
								'BOOKID' : book_id, 'EXCHANGEDATE' : date,
								'ISFINISHED' : 0, 'HASSUCCEEDED' : 0
				  	  		  }
				message = 'the request has been registered'
				Exchange.Exchange().insert(insert_dict)

	result = { 'status' : status, 'message' : message }

	return Controller.response_json(result)


@Routing.Route(url='/exchange/listoffers', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token')])
def list_offers(variables={}, request={}):
	status = 'success'
	message = ''

	token = request.params['token']

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	exchange_dict = Exchange.Exchange().query("USERNAME", "FIRSTNAME", "LASTNAME", "BOOKID", "TITLE", "GENRE"). \
					join("USERS", "RECEIVERID", "ID"). \
					join("BOOKS", "BOOKID", "ID"). \
					where("EXCHANGES.OWNERID", "=", user_dict[0]['USERID']). \
					condition("AND", "EXCHANGES.ISFINISHED", "=", 0).get()

	if(not exchange_dict):
		status = 'succes'
		message = 'no entries found'
		result = { 'status' : status, 'message' : message}
	else:
		status = 'succes'
		message = 'entries found'
		response = exchange_dict
		result = {'status' : status, 'message' : message, 'response' : response}

	return Controller.response_json(result)


@Routing.Route(url='/exchange/respond', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'bookid', 'accept')])
def accept_offer(variables={}, request={}):
	status = 'success'
	message = ''

	token = request.params['token']
	book_id = request.params['bookid']
	accept = request.params['accept']

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	book_dict = Book.Book().query("TITLE").where("ID", "=", book_id).get()

	if not book_dict:
		status = 'error'
		message = 'the book does not exist'
	else:
		exchange_dict = Exchange.Exchange().query("ISFINISHED").where("OWNERID", "=", user_dict[0]['USERID']). \
															    condition("AND", "BOOKID", "=", book_id).get()
		if not exchange_dict:
			status = 'error'
			message = 'the exchange does not exist'
		elif(exchange_dict[0]['ISFINISHED'] == 1):
			status = 'error'
			message = 'the exchange has already been approved/denied'
		else:
			status = 'success'
			message = 'a response has been assigned to the exchange request'
			Exchange.Exchange().update({ 'HASSUCCEEDED' : accept, 'ISFINISHED' : 1}).execute()

	result = { 'status' : status, 'message' : message }

	return Controller.response_json(result)