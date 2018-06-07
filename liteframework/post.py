import cgi


def get_post_form(environ):
    if 'REQUEST_METHOD' in environ and environ['REQUEST_METHOD'] == 'POST':
        input_data = environ['wsgi.input']
        post_form = environ.get('wsgi.post_form')
        if (post_form is not None
            and post_form[0] is input_data):
            return post_form[2]
        # This must be done to avoid a bug in cgi.FieldStorage
        environ.setdefault('QUERY_STRING', '')
        fs = cgi.FieldStorage(fp=input_data,
                              environ=environ,
                              keep_blank_values=1)
        new_input = InputProcessed()
        post_form = (new_input, input, fs)
        environ['wsgi.post_form'] = post_form
        environ['wsgi.input'] = new_input
        return fs
    return {}

class InputProcessed(object):
    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')
    readline = readlines = __iter__ = read