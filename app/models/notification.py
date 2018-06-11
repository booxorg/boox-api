import liteframework.model as Model

class Notification(Model.Model):
    table_name = 'NOTIFICATIONS'
    def __init__(self):
        Model.Model.__init__(self)
