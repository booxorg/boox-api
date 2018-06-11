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
								'BOOKID1' : book_id, 'EXCHANGEDATE' : date,
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


@Routing.Route(url='/exchange/decline-proposition', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'receiverid', 'bookid1')])
def decline_proposition(variables={}, request={}):
	status = 'success'
	message = ''

	token = request.params['token']
	book_id = request.params['bookid1']
	receiver_id = request.params['receiverid']

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	book_dict = Book.Book().query("TITLE").where("ID", "=", book_id).get()

	if not book_dict:
		status = 'error'
		message = 'the book does not exist'
	else:
		exchange_dict = Exchange.Exchange().query("*").where("OWNERID", "=", user_dict[0]['USERID']). \
													   condition("AND", "BOOKID1", "=", book_id). \
													   condition("AND", "RECEIVERID", "=", receiver_id).get()	

		if not exchange_dict:
			status = 'error'
			message = 'the exchange does not exist'
		else:
			if exchange_dict[0]['ISFINISHED'] == 1:
				status = 'error'
				message = 'the exchange has already been approved/denied'
			else:
				if exchange_dict[0]['BOOKID2'] != None:
					status = 'error'
					message = 'you cannot decline this exchange'
				else:
					Exchange.Exchange().update({ 'HASSUCCEEDED' : 0, 'ISFINISHED' : 1}). \
										where("OWNERID", "=", user_dict[0]['USERID']). \
									    condition("AND", "BOOKID1", "=", book_id). \
									    condition("AND", "RECEIVERID", "=", receiver_id).execute()

					status = 'success'
					message = 'the exchange has been declined'

	result = { 'status' : status, 'message' : message }

	return Controller.response_json(result)


@Routing.Route(url='/exchange/match-book', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'receiverid', 'bookid1', 'bookid2')])
def match_book(variables={}, request={}):
	status = 'succes'
	message = ''

	token = request.params['token']
	receiver_id = request.params['receiverid']
	book_id1 = request.params['bookid1']
	book_id2 = request.params['bookid2']	

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	book1_dict = Book.Book().query("TITLE").where("ID", "=", book_id1).get()
	book2_dict = Book.Book().query("TITLE").where("ID", "=", book_id2).get()

	if not book1_dict or not book2_dict:
		status = 'error'
		message = 'one of the books does not exist'
	else:
		exchange_dict = Exchange.Exchange().query("*").where("OWNERID", "=", user_dict[0]['USERID']). \
													   condition("AND", "BOOKID1", "=", book_id1). \
													   condition("AND", "RECEIVERID", "=", receiver_id).get()	

		if not exchange_dict:
			status = 'error'
			message = 'the exchange does not exist'	
		else:
			if exchange_dict[0]['ISFINISHED'] == 1:
				status = 'error'
				message = 'the exchange has already been approved/denied'
			else:
				if exchange_dict[0]['BOOKID2'] != None:
					status = 'error'
					message = 'you cannot respond to this exchange'
				else:
					Exchange.Exchange().update({ 'BOOKID2' : book_id2 }). \
										where("OWNERID", "=", user_dict[0]['USERID']). \
									    condition("AND", "BOOKID1", "=", book_id1). \
									    condition("AND", "RECEIVERID", "=", receiver_id).execute()

					status = 'success'
					message = 'user responded to the exchange'		

	result = { 'status' : status, 'message' : message }

	return Controller.response_json(result)			


@Routing.Route(url='/exchange/finish-exchange', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'ownerid', 'bookid1', 'bookid2', 'accept')])
def match_book(variables={}, request={}):
	status = 'error'
	message = ''

	token = request.params['token']
	owner_id = request.params['ownerid']
	book_id1 = request.params['bookid1']
	book_id2 = request.params['bookid2']
	accept = request.params['accept']

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	book1_dict = Book.Book().query("TITLE").where("ID", "=", book_id1).get()
	book2_dict = Book.Book().query("TITLE").where("ID", "=", book_id2).get()

	if not book1_dict or not book2_dict:
		status = 'error'
		message = 'one of the books does not exist'

	else:
		exchange_dict = Exchange.Exchange().query("*").where("RECEIVERID", "=", user_dict[0]['USERID']). \
													   condition("AND", "BOOKID1", "=", book_id1). \
													   condition("AND", "BOOKID2", "=", book_id2). \
													   condition("AND", "OWNERID", "=", owner_id).get()
		if not exchange_dict:
			status = 'error'
			message = 'the exchange does not exist'	
		else:
			if exchange_dict[0]['ISFINISHED'] == 1:
				status = 'error'
				message = 'the exchange has already been approved/denied'
			else:
					Exchange.Exchange().update({ 'ISFINISHED' : 1, 'HASSUCCEEDED' : accept }). \
										where("RECEIVERID", "=", user_dict[0]['USERID']). \
									    condition("AND", "BOOKID1", "=", book_id1). \
									    condition("AND", "BOOKID2", "=", book_id2). \
									    condition("AND", "OWNERID", "=", owner_id).execute()

					status = 'success'
					message = 'user responded to the exchange'		

	result = { 'status' : status, 'message' : message }

	return Controller.response_json(result)	
