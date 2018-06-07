import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import os
import base64
import liteframework.application as App

def encrypt(message, key=None):
    if not key:
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
    value = base64.b64encode(key.encrypt(message, 32)[0])
    return (key, value)

def import_key(key_name):
    keys_path = os.path.join(App.storage_path, 'keys')
    prv_path = os.path.join(keys_path, '%s_private.pem' % (key_name))
    pub_path = os.path.join(keys_path, '%s_public.pem' % (key_name))

    prv_key = None
    pub_key = None
    with open (prv_path, 'r') as prv_file:
        prv_key = RSA.importKey(prv_file.read())

    with open (pub_path, 'r') as pub_file:
        pub_key = RSA.importKey(pub_file.read())

    if (not prv_key) or (not pub_key):
        return None

    return (pub_key, prv_key)

def export_key(key, key_name):
    keys_path = os.path.join(App.storage_path, 'keys')
    prv_path = os.path.join(keys_path, '%s_private.pem' % (key_name))
    pub_path = os.path.join(keys_path, '%s_public.pem' % (key_name))
    with open (prv_path, 'w') as prv_file:
        prv_file.write(key.exportKey())

    with open (pub_path, 'w') as pub_file:
        pub_file.write(key.publickey().exportKey())

def decrypt(ciphertext, key):
    value = base64.b64decode(ciphertext)
    return key.decrypt(value)