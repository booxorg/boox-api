import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.middleware.params as Params
import app.models.user as User
import app.models.token as Token
import strgen
import bcrypt
import json

@Routing.Route(url='/login', method = 'GET', middleware=[Params.has_params('username', 'password')])
def register(variables={}, request={}):
    status = 'success'
    message = ''
        
    username = request.params['username']
    password = request.params['password']

    user = User.User()
    response_dict_user = user.query("ID").where("USERNAME", "=", username).condition("OR", "EMAIL", "=", username).get()
    if not response_dict_user:
        message = 'incorrect username or password'
        status = 'error'
    else:
        response_dict_pass = user.query("PASSWORD", "SALT").where("USERNAME", "=", username).condition("OR", "EMAIL", "=", username).get()
        input_pass_hash = bcrypt.hashpw(password.encode('utf8'), response_dict_pass[0]["SALT"])

        if(input_pass_hash != response_dict_pass[0]["PASSWORD"]):
            message = 'incorrect username or password'
            status = 'error'
        else:
            token = Token.Token()
            response_dict_token = token.query("TOKEN").where("USERID", "=", response_dict_user[0]["ID"]).condition("AND", "TOKENTYPE", "=", "booxtoken").get()
            message = 'log in successful'
            status = 'success'

    if(status == 'success'):
        response = { 'token' : response_dict_token[0]['TOKEN'] }
        result = {
            'status' : status,
            'message' : message,
            'response' : response
        }
    else:
        result = {
            'status' : status,
            'message' : message
        }

    return Controller.response_data(json.dumps(result), response_mimetype='text/json')
    