import liteframework.cookie as Cookie
import liteframework.application as App
import uuid as Unique
import os
import time
import pickle
from datetime import datetime

class Session:
    def __init__(self, request, expire = 1):
        self.expire = expire
        session_uuid = Cookie.get_cookie(request, 'session', None)
        if session_uuid:
            print 'Found session, loading'
            self.load(session_uuid, request)
        else:
            self.new(request)
        print 'session data, ', self.data
        self.cleanup()

    def cleanup(self):
        files_path = os.path.join(App.storage_path, 'session')
        for filename in os.listdir(files_path):
            try:
                full = os.path.join(files_path, filename)
                creation_date = datetime.fromtimestamp(os.path.getctime(full))
                current_date = datetime.now()
                diff = current_date - creation_date
                if diff.days > self.expire:
                    os.remove(full)
            except Exception, e:
                print 'Unable to verify session file ', filename
            
    def new(self, request):
        self.uuid = str(Unique.uuid4())
        self.data = {}
        self.save(request)

    def save(self, request):
        Cookie.set_cookie(request, 'session', self.uuid)
        file_path = os.path.join(App.storage_path, 'session', self.uuid)
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(self.__dict__, f)
        except Exception, e:
            print 'Failed to save session to file', repr(e)

    def load(self, uuid, request):
        self.uuid = uuid
        file_path = os.path.join(App.storage_path, 'session', self.uuid)
        try:
            with open(file_path, 'rb') as f:
                tmp_dict = pickle.load(f)
                self.__dict__.update(tmp_dict)
        except Exception, e:
            print 'Failed', repr(e)
            self.new(request)

    def get(self, key, default = None):
        if key in self.data:
            return self.data[key]
        else:
            return default
            
    def set(self, key, value):
        self.data.update({key : value})

    def flash(self, key, default = None):
        value = None
        if key in self.data:
            value = self.data[key]
            del self.data[key]
        else:
            value = default
        return value


