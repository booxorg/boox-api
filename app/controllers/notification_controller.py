import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.cookie as Cookie
import liteframework.middleware.params as Params
import app.middleware.token_valid as TokenCheck
import app.models.preference as Preference
import app.models.user as User
import app.models.token as Token
import app.models.location as Location
import app.models.notification as Notification
import liteframework.application as App
from math import sin, cos, sqrt, atan2, radians
import requests

#@Routing.Route(url='/notify', method='GET', middleware=[TokenCheck.token_valid, Params.has_params('token', 'bookname', 'bookid')])
def notify_users(token, bookname, bookid):
	status = 'success'
	message = ''

	#token = request.params['token']
	#bookname = request.params['bookname']
	#bookid = request.params['bookid']

	user_dict = Token.Token().query("USERID").where("TOKEN", "=", token).get()
	owner_location_dict = Location.Location().query("COUNTRY", "CITY", "VILLAGE", "STREET", "STREETNUMBER"). \
											where("USERID", "=", user_dict[0]['USERID']).get()

	owncountry = owner_location_dict[0]['COUNTRY']
	owncity = owner_location_dict[0]['CITY']
	ownvillage = owner_location_dict[0]['VILLAGE']
	ownstreet = owner_location_dict[0]['STREET']
	ownstreetnr = owner_location_dict[0]['STREETNUMBER']



	if owncountry == "" or owncity == "" or ownvillage == "" or ownstreet == "":
		status = 'error'
		message = 'the sender is missing location information'
	else:
		apiURL = "https://maps.google.com/maps/api/geocode/json?address="
		apiURL = "%s %s,%s,%s,%s" % (apiURL, owncountry, owncity, ownvillage, ownstreet)
		if ownstreetnr != "":
			apiURL = "%s %s" % (apiURL, ownstreetnr)
		apiURL = "%s&key=%s" % (apiURL, App.config.get('GOOGLE', 'geocoding_key'))

		api_response = requests.get(apiURL)
		api_status = api_response.json()['status']

		if api_status == 'ZERO_RESULTS':
			status = 'error'
			message = 'sender address not found'
		else:
			own_lat = api_response.json()['results'][0]['geometry']['location']['lat']
			own_lng = api_response.json()['results'][0]['geometry']['location']['lng']

			#print("owner %s %s") % (str(own_lat), str(own_lng))

			dict_preference = Preference.Preference().query("USERID").where("PREFERENCETYPE", "=", "bookname"). \
												      condition("AND","PREFERENCE", "=", bookname).get()

			for preference in dict_preference:
				location_dict = Location.Location().query("COUNTRY", "CITY", "VILLAGE", "STREET", "STREETNUMBER"). \
													where("USERID", "=", preference['USERID']).get()
				reccountry = location_dict[0]['COUNTRY']
				reccity = location_dict[0]['CITY']
				recvillage = location_dict[0]['VILLAGE']
				recstreet = location_dict[0]['STREET']
				recstreetnr = location_dict[0]['STREETNUMBER']

				if reccountry != "" and reccity != "" and recvillage != "" and recstreet != "":
					apiURL = "https://maps.google.com/maps/api/geocode/json?address="
					apiURL = "%s %s,%s,%s,%s" % (apiURL, reccountry, reccity, recvillage, recstreet)
					if ownstreetnr != "":
						apiURL = "%s %s" % (apiURL, recstreetnr)
					apiURL = "%s&key=%s" % (apiURL, App.config.get('GOOGLE', 'geocoding_key'))

					api_response = requests.get(apiURL)
					api_status = api_response.json()['status']

					if api_status != 'ZERO_RESULTS':
						rec_lat = api_response.json()['results'][0]['geometry']['location']['lat']
						rec_lng = api_response.json()['results'][0]['geometry']['location']['lng']
						
						#print "receiver %s %s" % (str(rec_lat), str(rec_lng))

						R = 6373.0
						lat1 = radians(own_lat)
						lon1 = radians(own_lng)
						lat2 = radians(rec_lat)
						lon2 = radians(rec_lng)

						dlat = lat2 - lat1
						dlon = lon2 - lon1

						a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
						c = 2 * atan2(sqrt(a), sqrt(1 - a))
						distance = R * c

						if(distance <= 5):
							dict_insert = { "BOOKID" : bookid, "OWNERID" : user_dict[0]['USERID'], 
											"RECEIVERID" : preference['USERID'] }
							Notification.Notification().insert(dict_insert)
					status = 'success'
					message = 'users have been notified'


	result = { 'status' : status, 'message' : message }

	return result
