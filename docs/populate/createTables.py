import MySQLdb


dbConnection = MySQLdb.connect("localhost", "root", "pass", "boox")
cursor = dbConnection.cursor()

query = """DROP TABLE IF EXISTS USERS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS LOCATIONS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS PREFERENCES;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS BOOKS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS AUTHORS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS USERBOOKS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS HISTORY;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS EXCHANGES;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS TOKENS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS NOTIFICATIONS;"""
cursor.execute(query)

query = """CREATE TABLE USERS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERNAME VARCHAR(20),
		   PASSWORD VARCHAR(60),
		   SALT VARCHAR(29),
		   FIRSTNAME VARCHAR(30),
		   LASTNAME VARCHAR(30),
		   EMAIL VARCHAR(30),
		   ISADMINISTRATOR BOOLEAN,
		   PRIMARY KEY(ID));"""

cursor.execute(query)


query = """CREATE TABLE LOCATIONS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   COUNTRY VARCHAR(100),
		   CITY VARCHAR(100),
		   STREET VARCHAR(100),
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, STREET) VALUES (1, "Romania", "Iasi", "Musatini")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, STREET) VALUES (2, "Romania", "Iasi", "Plaiesilor")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, STREET) VALUES (3, "Romania", "Iasi", "Stejar")"""
cursor.execute(query)


query = """CREATE TABLE PREFERENCES (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   PREFERENCETYPE VARCHAR(10),
		   PREFERENCE VARCHAR(20),
		   PRIMARY KEY(ID));"""

cursor.execute(query)


query = """CREATE TABLE EXCHANGES (
		   ID INT NOT NULL AUTO_INCREMENT,
		   OWNERID INT,
		   RECEIVERID INT,
		   BOOKID1 INT,
		   BOOKID2 INT,
		   EXCHANGEDATE DATE,
		   ISFINISHED BOOLEAN,
		   HASSUCCEEDED BOOLEAN,
		   PRIMARY KEY(ID));"""
cursor.execute(query)

query = """CREATE TABLE BOOKS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   GOODREADSID INT,
		   ISBN VARCHAR(13),
		   TITLE VARCHAR(100),
		   GENRE VARCHAR(10),
		   EXPIRES DATE,
		   AUTHORID INT,
		   COVER VARCHAR(100),
		   DELETED BOOLEAN,
		   PRIMARY KEY(ID));"""

cursor.execute(query)


query = """CREATE TABLE AUTHORS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   NAME VARCHAR(30),
		   PRIMARY KEY(ID));"""
cursor.execute(query)


query = """CREATE TABLE USERBOOKS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   BOOKID INT,
		   USERID INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)

query = """CREATE TABLE HISTORY (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   BOOKID INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)


query = """CREATE TABLE TOKENS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   TOKENTYPE VARCHAR(10),
		   TOKEN VARCHAR(20),
		   PRIMARY KEY(ID));"""
cursor.execute(query)


query = """CREATE TABLE NOTIFICATIONS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   BOOKID INT,
		   OWNERID INT,
		   RECEIVERID INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)

cursor.execute("COMMIT;")
