import liteframework.model as Model

class Book(Model.Model):
    table_name = 'BOOKS'
    def __init__(self):
        Model.Model.__init__(self)