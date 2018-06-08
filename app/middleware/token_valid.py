import liteframework.controller as Controller 
import app.models.token as Token

def token_valid(variables={}, request={}):
    status = 'success'
    message = ''
    token_ok = False

    if not 'token' in request.params:
        status = 'error'
        message = 'token must be present for this api'
    else:
        token = Token.Token()
        user_token = request.params['token']
        count = len(token.query('ID').where('TOKEN', '=', user_token).get())
        if count == 0:
            status = 'error'
            message = 'invalid user token'
        else:
            token_ok = True

    if token_ok:
        return (True, None)
    else:
        result = {
            'status' : status,
            'message' : message
        }
        return (False, Controller.response_json(result))

