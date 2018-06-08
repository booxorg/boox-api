import liteframework.model as Model

class User(Model.Model):
	table_name = 'USERS'
	def __init__(self):
		Model.Model.__init__(self)