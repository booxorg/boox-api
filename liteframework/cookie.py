from Cookie import SimpleCookie
import datetime
import uuid
import hmac
import liteframework.application as App
import liteframework.encryption as Encryption

def set_cookie(request, key, value, path='/', expires_after_days=30, domain=None):
    if not request.new_cookies:
        request.new_cookies = SimpleCookie()
    if not request.cookies:
        request.cookies = SimpleCookie()

    cookie_objects = [request.new_cookies, request.cookies]
    for cookie_object in cookie_objects:
        _, ciphertext = Encryption.encrypt(value, App.cookies_pub)
        cookie_object[key] = ciphertext
        cookie_object[key]['path'] = path

        # Set expiration time
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires_after_days) # expires in 30 days
        cookie_object[key]['expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Set domain
        if domain:
            cookie_object[key]['domain'] = domain



def get_cookie(request, key, default=None):
    if not key in request.cookies:
        return default
    else:
        value = request.cookies[key].value
        decrypted = Encryption.decrypt(value, App.cookies_prv)
        return decrypted

def delete_cookie(request, key):
    request.new_cookies[key] = ''
    request.new_cookies[key]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'