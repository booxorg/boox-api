import liteframework.model as Model

class Preference(Model.Model):
    table_name = 'PREFERENCES'
    def __init__(self):
        Model.Model.__init__(self)
