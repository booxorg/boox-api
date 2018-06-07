import MySQLdb

class Model:
	tableName = ""

	def __init__(self):
		self.query = ""

	def getConnectionCursor(self):
		dbConnection = MySQLdb.connect("localhost", "root", "pass", "boox")
		cursor = dbConnection.cursor()
		return cursor

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

	def where(self, columnName, operator, value):
		if(isinstance(value, basestring)):
			self.query = "%s WHERE %s %s \"%s\"" % (self.query, columnName, operator, value)
		else:
			self.query = "%s WHERE %s %s %s" % (self.query, columnName, operator, str(value))
		return self

	def addCondition(self, conditionType, columnName, operator, value):
		if(isinstance(value, basestring)):
			self.query = "%s %s %s %s \"%s\"" % (self.query, conditionType, columnName, operator, value)
		else:
			self.query = "%s %s %s %s %s" % (self.query, conditionType, columnName, operator, str(value))
		return self

	def addJoin(self, keyFirstTable, keySecondTable, joinTableName):
		self.query = "%s INNER JOIN %s ON %s.%s = %s.%s" % \
					 (self.query, joinTableName, self.tableName, keyFirstTable, joinTableName, keySecondTable)
		return self

	def addSort(self, sortType, sortKey):
		self.query = "%s ORDER BY %s %s" % (self.query, sortKey, sortType)
		return self

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

	def createUpdateQuery(self, dictInfo):
		self.query = "UPDATE %s SET " % (self.tableName)
		for key in dictInfo:
			if(isinstance(dictInfo[key], basestring)):
				self.query = "%s %s = \"%s\", " % (self.query, key, dictInfo[key])
			else:
				self.query = "%s %s = %s, " % (self.query, key, str(dictInfo[key]))

		self.query = self.query[:-2]
		return self

	def createDeleteQuery(self):
		self.query = "DELETE FROM %s " % (self.tableName)
		return self

	def executeQuery(self):
		cursor = self.getConnectionCursor()
		cursor.execute(self.query)
		cursor.execute("COMMIT;")

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


