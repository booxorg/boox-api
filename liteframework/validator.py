import re

def validate(values=[]):
    for (value, regex, message) in values:
        if not re.match(regex, value):
            return (False, message)
    return (True, None)