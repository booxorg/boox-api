import MySQLdb


dbConnection = MySQLdb.connect("localhost", "root", "root", "boox")
cursor = dbConnection.cursor()


query = """CREATE TABLE USERS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERNAME VARCHAR(20),
		   PASSWORD VARCHAR(60),
		   SALT VARCHAR(20),
		   FIRSTNAME VARCHAR(30),
		   LASTNAME VARCHAR(30),
		   EMAIL VARCHAR(30),
		   ISADMINISTRATOR BOOLEAN,
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("armandosexyguy", "$2a$12$WlxpMD6KfeoGsEydwX9v9enmm3sMCApDTyh9U90aGc14bd.Ge4wAy",
		   		  "kDH1rR6yc5UR8ZYkLxru", "Armando", "Ghedon", "garmando@gmail.com", 0)""" #password is password
cursor.execute(query)

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("proteinmuscleman29", "$2a$12$cXf7sWJ3xWawYaQxoxOsieR7EMAY7L88r1OpL7hms7JTd4sDxINBC",
		   		  "fMYY63TGYOvJI7Gr3Ux9", "Muscolo", "Mister", "mmuscolo@gmail.com", 0)""" #password is prafuri
cursor.execute(query)

query = """INSERT INTO USERS(USERNAME, PASSWORD, SALT, FIRSTNAME, LASTNAME, EMAIL, ISADMINISTRATOR)
		   VALUES("ladiesman69", "$2a$12$8os/YludCoo490dlDagUkeobuhTL9FarclztgGKeIaC2/l/0ua.Ye",
		   		  "jPN3kqtLoGNYKU70stib", "Casanova", "Amantu", "gigolou@gmail.com", 0)""" #password is boner
cursor.execute(query)

query = """CREATE TABLE LOCATIONS (
		   ID INT NOT NULL AUTO_INCREMENT,
		   USERID INT,
		   LOCATION VARCHAR(100),
		   PRIMARY KEY(ID));"""

cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, LOCATION) VALUES (1, "Iasi, Strada Bombei, nr. 512")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, LOCATION) VALUES (2, "Sangerei, Strada Denis, nr. 5")"""
cursor.execute(query)

query = """INSERT INTO LOCATIONS(USERID, LOCATION) VALUES (3, "Tzabana, Strada Tzaganului, nr. 69")"""
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
		   TITLE VARCHAR(30),
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
		   BOOKCOUNT INT,
		   PRIMARY KEY(ID));"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME, BOOKCOUNT) VALUES ("BOMBERMANE J. PHILLIPS", 1)"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME, BOOKCOUNT) VALUES ("BUFFY MCBUFFSON", 1)"""
cursor.execute(query)

query = """INSERT INTO AUTHORS(NAME, BOOKCOUNT) VALUES ("ADA LOVE", 1)"""
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
