import magic
import liteframework.application as App

########################################################
###
### Used for text or other simple responses 
### doesn't render anything, just determines dynamically
### the mimetype if it's not specified by the user
###
########################################################
def response_data(response_data, response_mimetype=None):
    if response_mimetype == None:
        response_mimetype = magic.from_buffer(response_data, mime = True)
    return (
        {
            'Content-type' : response_mimetype,
            'Content-Length' : str(len(response_data))
        },
        response_data.encode('utf-8'),
        '200 OK'
    )


def response_file(resource_url, response_mimetype=None):
    if resource_mimetype == None:
        resource_mimetype = magic.from_file(resource_url, mime = True)
    
    try:
        with open(resource_url, 'rb') as f:
            resource_data = f.read()
    except:
        resource_data = ''

    return (
        {
            'Content-type' : resource_mimetype,
            'Content-Length' : str(len(resource_data))
        },
        resource_data.encode('utf-8'),
        '200 OK'
    )


def response_not_found():
    response = '404, Not Found, Sowy'
    return (
        {
            'Content-type' : 'text/plain',
            'Content-Length' : str(len(response))
        },
        response.encode('utf-8'),
        '404 Not Found'
    )


def response_view(name, pass_variables = {}):
    template = App.jinja_env.get_template(name)
    response = template.render(**pass_variables)
    return (
        {
            'Content-type' : 'text/html',
            'Content-Length' : str(len(response))
        },
        response.encode('utf-8'),
        '200 OK'
    )


