import liteframework.cookie as Cookie
import liteframework.application as App
import uuid as Unique
import os
import time
import logging
import pickle
import liteframework.application as App 
from datetime import datetime

class Session:
    def __init__(self, request, expire = 1):
        if App.config.get('APP', 'store_sessions') == True:
            self.expire = expire
            session_uuid = Cookie.get_cookie(request, 'session', None)
            if session_uuid:
                self.load(session_uuid, request)
            else:
                self.new(request)
            self.cleanup()

    def cleanup(self):
        if App.config.get('APP', 'store_sessions') == True:
            files_path = os.path.join(App.storage_path, 'session')
            for filename in os.listdir(files_path):
                try:
                    full = os.path.join(files_path, filename)
                    creation_date = datetime.fromtimestamp(os.path.getctime(full))
                    current_date = datetime.now()
                    diff = current_date - creation_date
                    if diff.days > self.expire:
                        loggger.debug('Removing cache file: %s' % (full))
                        os.remove(full)
                except Exception, e:
                    logging.exception('Unable to remove old session file')
            
    def new(self, request):
        if App.config.get('APP', 'store_sessions') == True:
            self.uuid = str(Unique.uuid4())
            self.data = {}
            self.save(request)

    def save(self, request):
        if App.config.get('APP', 'store_sessions') == True:
            Cookie.set_cookie(request, 'session', self.uuid)
            file_path = os.path.join(App.storage_path, 'session', self.uuid)
            try:
                with open(file_path, 'wb') as f:
                    logging.debug('Saving session: %s' % (self.__dict__))
                    pickle.dump(self.__dict__, f)
            except Exception, e:
                logging.exception('Failed to save session to file')

    def load(self, uuid, request):
        if App.config.get('APP', 'store_sessions') == True:
            self.uuid = uuid
            file_path = os.path.join(App.storage_path, 'session', self.uuid)
            try:
                with open(file_path, 'rb') as f:
                    tmp_dict = pickle.load(f)
                    self.__dict__.update(tmp_dict)
                    self.save(request)
            except Exception, e:
                logging.exception('Failed to load session to file')
                self.new(request)

    def get(self, key, default = None):
        if App.config.get('APP', 'store_sessions') == True:
            if key in self.data:
                return self.data[key]
            else:
                return default
            
    def set(self, key, value):
        if App.config.get('APP', 'store_sessions') == True:
            self.data.update({key : value})

    def flash(self, key, default = None):
        if App.config.get('APP', 'store_sessions') == True:
            value = None
            if key in self.data:
                value = self.data[key]
                del self.data[key]
            else:
                value = default
            return value


