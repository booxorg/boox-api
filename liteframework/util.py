from urllib2 import quote 
import re
import posixpath

def url_reconstruction(environ):
    url = ''
    if environ['wsgi.url_scheme'] == 'https':
        if environ['SERVER_PORT'] != '443':
           url += ':' + environ['SERVER_PORT']
    else:
        if environ['SERVER_PORT'] != '80':
           url += ':' + environ['SERVER_PORT']

    url += quote(environ.get('SCRIPT_NAME', ''))
    url += quote(environ.get('PATH_INFO', ''))
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    return url

def match_url(template, actual_url):
    template = template.strip()
    actual_url = actual_url.strip()

    variables = {}
    variable = re.compile('{[^}]*::[^}]*}')
    while True:
        if variable.search(template):
            for m in re.finditer('({([^}]*::[^}]*)})', template):
                #Match part before variable
                print 'm1 {} m2 {}'.format(m.group(1), m.group(2))
                before = template[:m.start(1)]
                actual_before = actual_url[:len(before)]
                if before != actual_before:
                    return (False, {})
                actual_url = actual_url[len(before):]
                template = template[len(before):]

                print 'after strip {} // {}'.format(actual_url, template)
                # Match actual variable
                var = m.group(2)
                var_name, var_regex = var.split('::')
                match = re.match(var_regex, actual_url)
                if match:
                    actual_url = actual_url[match.span()[1]:]
                    template = template[len(m.group(1)):]
                else:
                    return (False, {})

                variables[var_name] = match.group()
        else:
            if template != actual_url:
                return (False, {})
            else:
                break

        if actual_url != '':
            return (False, {})
            
    return (True, variables)   
  