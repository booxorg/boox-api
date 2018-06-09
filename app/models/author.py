import liteframework.model as Model

class Author(Model.Model):
    table_name = 'AUTHORS'
    def __init__(self):
        Model.Model.__init__(self)