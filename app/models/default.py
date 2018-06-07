import liteframework.model as Model

class Default(Model.Model):
    table_name = 'default'
    def __init__(self):
        Model.Model.__init__(self)