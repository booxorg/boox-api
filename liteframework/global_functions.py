import liteframework.global_function as Global
import liteframework.application as App
##################################################################
###
### All the global default functions get declared here with a 
### special decorator defined in global_function.py
###
##################################################################


@Global.GlobalFunction
def full_url(relative_path):
    url = App.environ['wsgi.url_scheme']+'://'

    if App.environ.get('HTTP_HOST'):
        url += App.environ['HTTP_HOST']
    else:
        url += App.environ['SERVER_NAME']

    if App.environ['wsgi.url_scheme'] == 'https':
        if App.environ['SERVER_PORT'] != '443':
           url += ':' + environ['SERVER_PORT']
    else:
        if App.environ['SERVER_PORT'] != '80':
           url += ':' + App.environ['SERVER_PORT']

    relative_path = relative_path.strip()
    if not relative_path.startswith('/'):
        relative_path = '/' + relative_path
    url += relative_path
    
    return url

@Global.GlobalFunction
def session(key, default=None):
    return App.session.get(key, default)