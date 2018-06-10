import liteframework.model as Model

class Location(Model.Model):
    table_name = 'LOCATIONS'
    def __init__(self):
        Model.Model.__init__(self)