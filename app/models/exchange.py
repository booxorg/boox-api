import liteframework.model as Model

class Exchange(Model.Model):
    table_name = 'EXCHANGES'
    def __init__(self):
        Model.Model.__init__(self)