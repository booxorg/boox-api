import MySQLdb

class Model:
	tableName = ""

	def __init__(self):
		self.query = ""

	def getConnectionCursor(self):
		dbConnection = MySQLdb.connect("localhost", "root", "pass", "boox")
		cursor = dbConnection.cursor()
		return cursor

	#Creates a SELECT query. If * is provided, it searches and replaces * with all the table's columns
	def createSelectQuery(self, *columnNames):
		self.query = "SELECT ";

		if(columnNames[0] == "*"):
			cursor = self.getConnectionCursor();
			cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'boox' AND TABLE_NAME = " + "\"" + self.tableName + "\"");
			results = cursor.fetchall()
			for row in results:
				self.query = self.query + row[0] + ","			

		else:
			for column in columnNames:
				self.query = self.query + column + ","

		self.query = self.query[:-1]
		self.query = "%s FROM %s" % (self.query, self.tableName)
		
		return self

	#Adds a where clause
	def where(self, columnName, operator, value):
		if(isinstance(value, basestring)):
			self.query = "%s WHERE %s %s \"%s\"" % (self.query, columnName, operator, value)
		else:
			self.query = "%s WHERE %s %s %s" % (self.query, columnName, operator, str(value))
		return self

	#Adds an AND or OR condition to the query
	def addCondition(self, conditionType, columnName, operator, value):
		if(isinstance(value, basestring)):
			self.query = "%s %s %s %s \"%s\"" % (self.query, conditionType, columnName, operator, value)
		else:
			self.query = "%s %s %s %s %s" % (self.query, conditionType, columnName, operator, str(value))
		return self

	#Adds a join, keyFirstTable is the key from the tableName table 
	def addJoin(self, keyFirstTable, keySecondTable, joinTableName):
		self.query = "%s INNER JOIN %s ON %s.%s = %s.%s" % \
					 (self.query, joinTableName, self.tableName, keyFirstTable, joinTableName, keySecondTable)
		return self

	#Sorts the values based on sortKey. sortType can be ASC, DESC
	def addSort(self, sortType, sortKey):
		self.query = "%s ORDER BY %s %s" % (self.query, sortKey, sortType)
		return self

	#Inserts a line into the table. You must provide a dictionary in the following format {column_name : value, ...}
	def insertInfo(self, dictInfo):
		self.query = "INSERT INTO %s (" % (self.tableName)
		for key in dictInfo:
			self.query = "%s %s, " % (self.query, key)

		self.query = "%s) VALUES (" % (self.query[:-2])

		for key in dictInfo:
			if(isinstance(dictInfo[key], basestring)):
				self.query = "%s \"%s\", " % (self.query, dictInfo[key])
			else:
				self.query = "%s %s, " % (self.query, str(dictInfo[key]))

		self.query = "%s)" % (self.query[:-2])

		cursor = self.getConnectionCursor()
		cursor.execute(self.query)
		cursor.execute("COMMIT;")

	#Creates an update query. It can be used in combination with where. 
	def createUpdateQuery(self, dictInfo):
		self.query = "UPDATE %s SET " % (self.tableName)
		for key in dictInfo:
			if(isinstance(dictInfo[key], basestring)):
				self.query = "%s %s = \"%s\", " % (self.query, key, dictInfo[key])
			else:
				self.query = "%s %s = %s, " % (self.query, key, str(dictInfo[key]))

		self.query = self.query[:-2]
		return self

	#Creates a delete query. It can be used in combination with where.
	def createDeleteQuery(self):
		self.query = "DELETE FROM %s " % (self.tableName)
		return self

	#Used for executing the query after creating an update or delete query
	def executeQuery(self):
		cursor = self.getConnectionCursor()
		cursor.execute(self.query)
		cursor.execute("COMMIT;")

	#Returns the result of a query as a dictionary {column_name : value, ...}. Must be used only with createSelectQuery
	def getResult(self):
		cursor = self.getConnectionCursor()
		cursor.execute(self.query)
		results = cursor.fetchall()

		dictKeys = self.query.split()[1].split(",")
		dictList = []

		for row in results:
			currentDict = {}
			for i in range(len(row)):
				currentDict[dictKeys[i]] = row[i]
			dictList.append(currentDict)
		
		return dictList	

"""
Examples: 

suppose we have the class User which is a subclass of Model and has tableName set to "USERS"

obj = User()
result = obj.createSelectQuery("USERNAME", "PASSWORD").where("ID", ">", "2").getResult()

obj.insertInfo({"USERNAME" : "armando", "PASSWORD" : "fuego"})
obj.createUpdateQuery(*your dict here*).where(*your condition here*).executeQuery()
obj.createDeleteQuery().where(*your condition here*).executeQuery()
"""
