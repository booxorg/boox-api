import liteframework.model as Model

class Token(Model.Model):
	table_name = 'TOKENS'
	def __init__(self):
		Model.Model.__init__(self)