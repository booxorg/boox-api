import MySQLdb
from operator import itemgetter
import liteframework.application as App
import re

class Model:
	table_name = ""
	escaped_column_names = []
	column_names = []

	def __init__(self):
		self.__query = ""
		self.__database = App.config.get('DATABASE', 'database')
		self.__username = App.config.get('DATABASE', 'username')
		self.__password = App.config.get('DATABASE', 'password')
		self.__db_address = App.config.get('DATABASE', 'db_address')

	def __get_connection_cursor(self):
		dbConnection = MySQLdb.connect(
			self.__db_address, 
			self.__username,
			self.__password, 
			self.__database
		)
		cursor = dbConnection.cursor()
		return cursor

	def __commit(self):
		cursor = self.__get_connection_cursor()
		cursor.execute("COMMIT;")

	def __execute(self, sql):
		cursor = self.__get_connection_cursor();
		print sql
		#sql = MySQLdb.escape_string(sql)
		cursor.execute(sql);
		return cursor.fetchall()

	def __column_escape(self, column_name):
		return re.sub(r'([^.]*)\.([^.]*)', r'`\1`.\2', column_name)

	#Creates a SELECT query. If * is provided, it searches and replaces * with all the table's columns
	def query(self, *column_names):

		if(column_names[0] == '*'):
			cursor = self.__get_connection_cursor();
			sql = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s' % (self.__database, self.table_name)
			results = self.__execute(sql)
			self.column_names = map(itemgetter(0), results)
		else:
			self.column_names = column_names

		self.escaped_column_names = [self.__column_escape(column) for column in self.column_names]
		self.__query = "SELECT %s FROM `%s`" % (', '.join(self.escaped_column_names), self.table_name)
		return self

	#Adds a where clause
	def where(self, column_name, operator, value):
		if(isinstance(value, basestring)):
			self.__query = '%s WHERE %s %s "%s"' % (self.__query, self.__column_escape(column_name), operator, value)
		else:
			self.__query = '%s WHERE %s %s %s' % (self.__query, self.__column_escape(column_name), operator, str(value))
		return self

	#Adds an AND or OR condition to the query
	def condition(self, condition_type, column_name, operator, value):
		if(isinstance(value, basestring)):
			self.__query = "%s %s %s %s \"%s\"" % (self.__query, condition_type, column_name, operator, value)
		else:
			self.__query = "%s %s %s %s %s" % (self.__query, condition_type, column_name, operator, str(value))
		return self

	#Adds a join, keyFirstTable is the key from the table_name table 
	def join(self, other_table_name, current_table_key, other_table_key):
		self.__query = "%s INNER JOIN %s ON %s.%s = %s.%s" % \
					 (self.__query, other_table_name, self.table_name, current_table_key, other_table_name, other_table_key)
		return self

	#Sorts the values based on sortKey. sortType can be ASC, DESC
	def sort(self, key, order='ASC'):
		self.__query = "%s ORDER BY %s %s" % (self.__query, key, order)
		return self

	#Inserts a line into the table. You must provide a dictionary in the following format {column_name : value, ...}
	def insert(self, column_values):
		columns = column_values.keys()
		values = []
		
		for (key, value) in column_values.iteritems():
			if(isinstance(value, basestring)):
				values.append('"%s"' % (value))
			else:
				values.append('%s' % (str(value)))

		self.__query = 'INSERT INTO `%s` (%s) VALUES (%s)' % (self.table_name, ', '.join(columns), ', '.join(values))
		self.__execute(self.__query)
		return None

	#Creates an update query. It can be used in combination with where. 
	def update(self, column_values):
		columns = column_values.keys()
		values = []
		
		for (key, value) in column_values.iteritems():
			if(isinstance(value, basestring)):
				values.append('%s = "%s"' % (key, value))
			else:
				values.append('%s = %s' % (key, str(value)))

		self.__query = 'UPDATE %s SET %s' % (self.table_name, ', '.join(values))
		return self

	#Creates a delete query. It can be used in combination with where.
	def delete(self):
		self.__query = "DELETE FROM %s " % (self.table_name)
		return self

	#Used for executing the query after creating an update or delete query
	def execute(self):
		self.__execute(self.__query)
		return self

	#Returns the result of a query as a dictionary {column_name : value, ...}. Must be used only with query
	def get(self):
		results = self.__execute(self.__query)
		print results, self.column_names
		dict_list = []
		for row in results:
			current_result = {}
			for i in range(len(row)):
				current_result.update({self.column_names[i]: row[i]})
			dict_list.append(current_result)
		
		return dict_list	

"""
Examples: 

suppose we have the class User which is a subclass of Model and has table_name set to "USERS"

obj = User()
result = obj.query("USERNAME", "PASSWORD").where("ID", ">", "2").getResult()

obj.insert({"USERNAME" : "armando", "PASSWORD" : "fuego"})
obj.update(*your dict here*).where(*your condition here*).execute()
obj.delete().where(*your condition here*).execute()
"""
