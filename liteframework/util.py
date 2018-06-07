import liteframework.global_function as global_function
from urllib2 import quote 
import re
import posixpath

def url_reconstruction(environ):
    url = ''    
    url += quote(environ.get('SCRIPT_NAME', ''))

    url += quote(environ.get('PATH_INFO', ''))
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    return url


def match_url(template, actual_url):
    print template, actual_url
    template = template.strip()
    actual_url = actual_url.strip()

    template_parts = template.split('/')
    actual_parts = actual_url.split('/')
    if len(template_parts) != len(actual_parts):
        return (False, {})

    variables = {}
    variable = re.compile('{[^}]*::[^}]*}')
    for template_part, actual_part in zip(template_parts, actual_parts):
        if variable.search(template_part):
            for m in re.finditer('({([^}]*::[^}]*)})', template_part):
                #Match part before variable
                before = template_part[:m.start(1)]
                actual_before = actual_part[:len(before)]
                if before != actual_before:
                    return (False, {})
                actual_part = actual_part[len(before):]
                template_part = template_part[len(before):]

                # Match actual variable
                var = m.group(2)
                var_name, var_regex = var.split('::')
                match = re.match(var_regex, actual_part)
                if match:
                    actual_part = actual_part[match.span()[1]:]
                    template_part = template_part[len(m.group(1)):]
                else:
                    return (False, {})

                variables[var_name] = match.group()
            if actual_part != '':
                return (False, {})
        else:
            if template_part != actual_part:
                return (False, {})


            
    return (True, variables)   
