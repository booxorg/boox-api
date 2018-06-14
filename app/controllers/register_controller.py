import liteframework.controller as Controller 
import liteframework.routing as Routing 
import liteframework.middleware.params as Params
import liteframework.validator as Validator
import app.models.user as User
import app.models.token as Token
import strgen
import bcrypt
import json
import logging

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

    ok, error_message = Validator.validate([
        (username, r'^[A-Za-z][A-Za-z0-9]+$', 'The username should be only small and big letters with numbers'),
        (password, r'^.{7,}$', 'Password should be longer than 6 characters'),
        (cpassword, r'^.{7,}$', 'Password confirm should be longer than 6 characters'),
        (fname, r'^[\w,-\']+$', 'first name value is invalid'),
        (lname, r'^[\w,-\']+$', 'last name value is invalid'),
        (email, r"""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""", 'email value is invalid'),
    ])

    try:
        if not ok:
            raise UserWarning(error_message)

        user = User.User()
        token = Token.Token()
        response_dict_list = user.query("ID").where("USERNAME", "=", username).condition("OR", "EMAIL", "=", email).get()
        if not response_dict_list:
            if(password != cpassword):
                raise UserWarning('passwords do no match')
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
            raise UserWarning('username already exists')

    except UserWarning, e:
        logging.exception('User warning')
        return Controller.response_json({
            'status' :  'error',
            'message' : str(e)   
        })
    except Exception, e:
        logging.exception('Fatal error')
        return Controller.response_json({
            'status' :  'error',
            'message' : 'fatal error occured'   
        })

    return Controller.response_json({
        'status' : 'success',
        'message' : 'register sucessful',
        'response' : result    
    })