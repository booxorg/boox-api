import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.middleware.params as Params
import app.models.user as User
import app.models.token as Token
import strgen
import bcrypt
import json

@Routing.Route(url='/register', method = 'GET', middleware=[Params.has_params('username', 'password', 'fname', 'lname', 'email', 'cpassword')])
def register(variables={}, request={}):
    status = 'success'
    message = ''
        
    username = request.params['username']
    password = request.params['password']
    cpassword = request.params['cpassword']
    fname = request.params['fname']
    lname = request.params['lname']
    email = request.params['email']

    user = User.User()
    token = Token.Token()
    response_dict_list = user.query("ID").where("USERNAME", "=", username).condition("OR", "EMAIL", "=", email).get()
    if not response_dict_list:
        if(password != cpassword):
            message = 'passwords do not match'
            status = 'error'
        else:
            generated_token = strgen.StringGenerator("[\w\d]{20}").render()
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf8'), salt)
            insert_user_dict = {
                "USERNAME" : username, 
                "PASSWORD" : password_hash, 
                "SALT" : salt, 
                "FIRSTNAME" : fname,
                "LASTNAME" : lname, 
                "EMAIL" : email,
                "ISADMINISTRATOR" : 0
            }
            inserted_user = user.insert(insert_user_dict)
            
            insert_token_dict = {
                "USERID" : inserted_user["ID"], 
                "TOKENTYPE" : "booxtoken",
                "TOKEN" : generated_token
            }
            token.insert(insert_token_dict)

            message = 'user registered successfully'
    else:
        message = 'username already exists'
        status = 'error'

    result = {
        'status' : status,
        'message' : message
    }

    return Controller.response_data(json.dumps(result), response_mimetype='text/json')
    