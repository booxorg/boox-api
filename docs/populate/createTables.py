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
query = """DROP TABLE IF EXISTS COVERS;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS HISTORY;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS EXCHANGES;"""
cursor.execute(query)
query = """DROP TABLE IF EXISTS TOKENS;"""
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

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("armandosexyguy", "$2b$12$L5/Ow/BUmwE7cg51ZBCYZe3SF/jmw3dFfqtQrRcjQ/CW79fknbFWW",
		   		  "$2b$12$L5/Ow/BUmwE7cg51ZBCYZe", "Armando", "Ghedon", "garmando@gmail.com", 0)""" #password is password
cursor.execute(query)

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("proteinmuscleman29", "$2b$12$HhH5LGXEqQF9KuAm4pJCjOCch6wifMKQY06trbHBcDzpZ8plYmZK6",
		   		  "$2b$12$HhH5LGXEqQF9KuAm4pJCjO", "Muscolo", "Mister", "mmuscolo@gmail.com", 0)""" #password is prafuri
cursor.execute(query)

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("ladiesman69", "$2b$12$6KfM2W6iFUlnbEEcBPkB8.cSXXv8qgmJ.0KSbTlDwFeEKch9lJrua",
		   		  "$2b$12$6KfM2W6iFUlnbEEcBPkB8.", "Casanova", "Amantu", "gigolou@gmail.com", 0)""" #password is boner
cursor.execute(query)

query = """CREATE TABLE LOCATIONS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   COUNTRY VARCHAR(100),
		   CITY VARCHAR(100),
		   VILLAGE VARCHAR(100),
		   STREET VARCHAR(100),
		   STREETNUMBER VARCHAR(10),
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, VILLAGE, STREET, STREETNUMBER) VALUES (1, "Romania", "Iasi", "", "Musatini", "55")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, VILLAGE, STREET, STREETNUMBER) VALUES (2, "Romania", "Iasi", "", "Plaiesilor", "55")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, COUNTRY, CITY, VILLAGE, STREET, STREETNUMBER) VALUES (3, "Romania", "Iasi", "", "Stejar", "41")"""
cursor.execute(query)


query = """CREATE TABLE PREFERENCES (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   PREFERENCETYPE VARCHAR(10),
		   PREFERENCE VARCHAR(20),
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO PREFERENCES(USERID, PREFERENCETYPE, PREFERENCE) VALUES (1, "GENRE", "SCI-FI")"""
cursor.execute(query)

query = """INSERT INTO PREFERENCES(USERID, PREFERENCETYPE, PREFERENCE) VALUES (2, "GENRE", "FITNESS")"""
cursor.execute(query)

query = """INSERT INTO PREFERENCES(USERID, PREFERENCETYPE, PREFERENCE) VALUES (3, "GENRE", "ROMANCE")"""
cursor.execute(query)


query = """CREATE TABLE BOOKS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   ISBN VARCHAR(13),
		   TITLE VARCHAR(100),
		   GENRE VARCHAR(10),
		   EXPIRES DATE,
		   AUTHORID INT,
		   COVERID INT,
		   DELETED BOOLEAN,
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO BOOKS (ISBN, TITLE, GENRE, EXPIRES, AUTHORID, COVERID, DELETED)
		   VALUES(1111111111111, "Abstract bombs", "SCI-FI", "2018-10-20", 1, 1, 0)"""
cursor.execute(query)

query = """INSERT INTO BOOKS (ISBN, TITLE, GENRE, EXPIRES, AUTHORID, COVERID, DELETED)
		   VALUES(2222222222222, "Do you even lift, bro?", "FITNESS", "2018-10-21", 2, 2, 0)"""
cursor.execute(query)

query = """INSERT INTO BOOKS (ISBN, TITLE, GENRE, EXPIRES, AUTHORID, COVERID, DELETED)
		   VALUES(3333333333333, "How to treat gurls", "LIFESTYLE", "2018-10-23", 3, 3, 0)"""
cursor.execute(query)


query = """CREATE TABLE AUTHORS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   NAME VARCHAR(30),
		   PRIMARY KEY(ID));"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME) VALUES ("BOMBERMANE J. PHILLIPS")"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME) VALUES ("BUFFY MCBUFFSON")"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME) VALUES ("ADA LOVE")"""
cursor.execute(query)


query = """CREATE TABLE USERBOOKS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   BOOKID INT,
		   USERID INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)

query = """INSERT INTO USERBOOKS(BOOKID, USERID) VALUES (1, 1)"""
cursor.execute(query)

query = """INSERT INTO USERBOOKS(BOOKID, USERID) VALUES (2, 2)"""
cursor.execute(query)

query = """INSERT INTO USERBOOKS(BOOKID, USERID) VALUES (3, 3)"""
cursor.execute(query)

query = """CREATE TABLE COVERS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   COVER MEDIUMBLOB,
		   PRIMARY KEY(ID));"""
cursor.execute(query)


query = """CREATE TABLE HISTORY (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   BOOKID INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)


query = """CREATE TABLE EXCHANGES (
		   ID INT NOT NULL AUTO_INCREMENT,
		   OWNERID INT,
		   RECEIVERID INT,
		   BOOKID INT,
		   EXCHANGEDATE DATE,
		   ISFINISHED BOOLEAN,
		   HASSUCCEEDED BOOLEAN,
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
