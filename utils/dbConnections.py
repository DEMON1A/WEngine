'''
to keep WEngine project simple, i'm about to create a simple
python code that gonna help you interacting with the databases
using SQLite and to be able to deal with your data from your
application routes. instead of implementing the same
functions over again every single project

this util also comes with SQL injection protections to avoid
any security issues on the code.

but it's vulnerable at the time of wrting this, so if you gonna deal with
any user input. please filter it before it.
'''

import sqlite3
from os.path import exists
from os import mkdir
from config.db import __DB_BASE_FOLDER__

def validateFolder():
    if exists(__DB_BASE_FOLDER__):
        pass
    else:
        mkdir(__DB_BASE_FOLDER__)

def parseConfig(dbConfig):
    if type(dbConfig) != dict:
        return False
    else:
        SQLstring = ""

        for name,_type in dbConfig.items():
            SQLstring += f"{name} {_type}, "

        SQLstring = SQLstring[:-2]
        return SQLstring

def insertParser(dbConfig):
    inputsCount = len(dbConfig)
    questionMarkString = ""

    while inputsCount != 0:
        questionMarkString += "?,"
        inputsCount -= 1

    questionMarkString = questionMarkString[:-1]
    return questionMarkString

def searchQuery(dbConfig):
    qstring = ""
    for name,value in dbConfig.items():
        qstring += f"{name}=? or "

    return qstring[:-3]

def getdbname(dbname):
    validateFolder()
    dbname = f"{__DB_BASE_FOLDER__}/{dbname}"
    dbname = dbname.replace('..', '').replace('//', '/')

    return dbname

def createDB(dbname):
    dbname = getdbname(dbname)
    dbConnection = sqlite3.connect(dbname)
    dbConnection.close()

def createTable(dbname, tablename, dbConfig):
    dbname = getdbname(dbname)

    dbConnection = sqlite3.connect(dbname)
    dbExecution = dbConnection.cursor()

    SQLConfig = parseConfig(dbConfig=dbConfig)
    dbExecution.execute(f"CREATE TABLE IF NOT EXISTS {tablename} (id INTEGER PRIMARY KEY, {SQLConfig})")

    dbConnection.commit()
    dbConnection.close()

def appendData(dbname, tablename, dbConfig):
    dbname = getdbname(dbname)

    dbConnection = sqlite3.connect(dbname)
    dbExecution = dbConnection.cursor()

    questionMarks = insertParser(dbConfig=dbConfig)
    dbExecution.execute(f"INSERT INTO {tablename} VALUES(NULL,{questionMarks})", dbConfig)

    dbConnection.commit()
    dbConnection.close()

def search(dbname, tablename, dbConfig, variables):
    dbname = getdbname(dbname)

    dbConnection = sqlite3.connect(dbname)
    dbExecution = dbConnection.cursor()

    SQLsyntax = searchQuery(dbConfig)
    dbExecution.execute(f"SELECT * FROM {tablename} WHERE {SQLsyntax}", variables)
    dbData = dbExecution.fetchall()

    return dbData

def showAll(dbname, tablename):
    dbname = getdbname(dbname)

    dbConnection = sqlite3.connect(dbname)
    dbExecution = dbConnection.cursor()

    dbExecution.execute(f"SELECT * FROM {tablename}")
    dbData = dbExecution.fetchall()
    dbConnection.close()

    return dbData

def execQuery(dbname, SQLCommand):
    dbname = getdbname(dbname)
    dbConnection = sqlite3.connect(dbname)
    dbExecution = dbConnection.cursor()

    dbExecution.execute(f"{SQLCommand}")
    dbData = dbExecution.fetchall()
    dbConnection.close()

    return dbData
