import liteframework.model as Model

class UserBook(Model.Model):
    table_name = 'USERBOOKS'
    def __init__(self):
        Model.Model.__init__(self)