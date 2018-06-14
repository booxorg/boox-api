import MySQLdb
from operator import itemgetter
import liteframework.application as App
import re, logging

class Model:
	table_name = ""
	escaped_column_names = []
	column_names = []
	db_connection = None

	def __init__(self):
		self.__query = ""
		self.__database = App.config.get('DATABASE', 'database')
		self.__username = App.config.get('DATABASE', 'username')
		self.__password = App.config.get('DATABASE', 'password')
		self.__db_address = App.config.get('DATABASE', 'db_address')
		self.primary_key = App.config.get('DATABASE', 'primary_key')

	def __del__(self):
		if self.db_connection:
			self.db_connection.commit()
			self.db_connection.close()

	def __get_connection_cursor(self):
		if not self.db_connection:
			self.db_connection = MySQLdb.connect(
				self.__db_address, 
				self.__username,
				self.__password, 
				self.__database
			)
		cursor = self.db_connection.cursor()
		return cursor

	def __commit(self):
		cursor = self.__get_connection_cursor()
		self.db_connection.commit()
		cursor.execute("COMMIT;")

	def __execute(self, sql):
		cursor = self.__get_connection_cursor()
		#print sql
		#sql = MySQLdb.escape_string(sql)
		cursor.execute(sql);
		return cursor.fetchall()

	def __resolve_column_names(self, *column_names):
		if column_names[0] == '*':
			cursor = self.__get_connection_cursor();
			sql = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "%s" AND TABLE_NAME = "%s"' % (self.__database, self.table_name)
			results = self.__execute(sql)
			return map(itemgetter(0), results)
		else:
			return column_names

	def __get_last_row(self):
		last_id = int(self.__execute('SELECT LAST_INSERT_ID()')[0][0])
		self.__query = 'SELECT * FROM `%s` WHERE %s = %d' % (self.table_name, self.primary_key, last_id)
		result = self.__execute(self.__query)
		return self.__match_results(result[0], self.__resolve_column_names('*'))

	def __match_results(self, results, columns):
		return dict(zip(columns, results))

	def __column_escape(self, column_name):
		if not '.' in column_name:
			return '`%s`.%s' % (self.table_name, column_name)
		return column_name

	#Creates a SELECT query. If * is provided, it searches and replaces * with all the table's columns
	def query(self, *column_names):
		self.column_names = self.__resolve_column_names(*column_names)
		self.escaped_column_names = [self.__column_escape(column) for column in self.column_names]
		self.__query = "SELECT %s FROM `%s`" % (', '.join(self.escaped_column_names), self.table_name)
		return self

	def count(self):
		self.__query = "SELECT COUNT(*) FROM `%s`" % (self.table_name)
		self.column_names = ['count']
		return self

	#Adds a where clause
	def where(self, column_name, operator, value):
		if(isinstance(value, basestring)):
			self.__query = '%s WHERE %s %s "%s"' % (self.__query, self.__column_escape(column_name), operator, value)
		else:
			self.__query = '%s WHERE %s %s %s' % (self.__query, self.__column_escape(column_name), operator, str(value))
		return self

	def whereAll(self, values):
		self.__query += ' WHERE ';
		preps = []
		for (name, operator, value) in values:
			if(isinstance(value, basestring)):
				preps.append('(%s %s "%s")' % (self.__column_escape(name), operator, value))
			else:
				preps.append('(%s %s %s)' % (self.__column_escape(name), operator, str(value)))

		self.__query += 'AND'.join(preps)
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

		self.__query = 'INSERT INTO %s (%s) VALUES (%s);' % (self.table_name, ', '.join(columns), ', '.join(values))
		self.__execute(self.__query)
		self.__commit()
		return self.__get_last_row()

	def update_or_create(self, to_match, column_values):
		self.query('*')
		self.whereAll([(key, '=', value) for (key, value) in to_match.iteritems()])
		results = self.get()
		if len(results) > 0:
			self.update(column_values)
			for (key, value) in to_match.iteritems():
				self.whereAll([(key, '=', value) for (key, value) in to_match.iteritems()])
			self.execute()
			return self.__get_last_row()
		else:
			return self.insert(column_values)

	#Creates an update query. It can be used in combination with where. 
	def update(self, column_values):
		columns = column_values.keys()
		values = []
		
		for (key, value) in column_values.iteritems():
			if(isinstance(value, basestring)):
				values.append('%s = "%s"' % (key, value))
			else:
				values.append('%s = %s' % (key, str(value)))

		self.__query = 'UPDATE %s SET %s,%s=LAST_INSERT_ID(%s)' % (self.table_name, ', '.join(values), self.primary_key, self.primary_key)
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
		final_list = []
		for result in results:
			final_list.append(self.__match_results(result, self.column_names))
		return final_list

"""
Examples: 

suppose we have the class User which is a subclass of Model and has table_name set to "USERS"

obj = User()
result = obj.query("USERNAME", "PASSWORD").where("ID", ">", "2").getResult()

obj.insert({"USERNAME" : "armando", "PASSWORD" : "fuego"})
obj.update(*your dict here*).where(*your condition here*).execute()
obj.delete().where(*your condition here*).execute()
"""
