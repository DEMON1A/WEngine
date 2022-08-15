'''
while creating your tool mode the class name should be the
same as the command name and the main function inside of the class
should be the same as them. it should take one argument with anyname 
but to keep stuff simple use the variable 'serverConfig' to avoid
changing the main pattern of the application.

you can always create more functions inside of the mode class but you should call
all of them inside of the main function that has the same name as the class
'''
class runserver:
    def __init__(self):
        pass

    def runserver(self, serverConfig):
        serverPort = serverConfig['SERVER_PORT']
        defaultDocument = serverConfig['DEFAULT_DOCUMENT']

        from HTTPServer.mainServer import serveServer
        serveServer(serverPort=serverPort, defaultDocument=defaultDocument)


class checkstatic:
    def __init__(self):
        pass

    def checkstatic(self, serverConfig):
        staticPath = serverConfig['STATIC_PATH']
        from os.path import exists
        from os import mkdir

        if exists(staticPath):
            from utils.showMessage import showGood
            showGood(goodRule="Static Found" , Message=f"The static path your provided '{staticPath}' has been found")
        else:
            from utils.showMessage import showError, askForInput, showGood
            showError(exceptionRule="Path Error", Message="We couldn't validate the static path you provided. make sure you're running it from the home dir.")
            
            userInput = askForInput(userMessage="If you're sure you did run this tool from the home dir, would you like to create the static folder? ")
            if userInput.lower() == "y" or userInput.lower() == "yes":
                mkdir(staticPath)
                showGood(goodRule="Folder Created", Message=f"The static folder '{staticPath}' has been created")
            else:
                pass

class cleanlogs:
    def __init__(self):
        pass

    def cleanlogs(self, serverConfig):
        from utils.logsController import cleanServerLogs
        if cleanServerLogs():
            from utils.showMessage import showGood
            showGood(goodRule="Cleaned", Message="Logs has been cleaned and now the logs data is empty.")
        else:
            pass

class migrate:
    def __init__(self):
        pass

    def migrate(self, serverConfig):
        from utils.dbConnections import createDB, createTable
        from utils.showMessage import showGood, showError
        from config.db import __DEFAULT_DB_NAME__, __DEFAULT_DB_TABLE__, __DEFAULT_DB_CONFIG__

        try:
            createDB(dbname=__DEFAULT_DB_NAME__)
            showGood(goodRule="DB created", Message=f"{__DEFAULT_DB_NAME__} has been created successfully")
        except Exception as e:
            showError(exceptionRule="DB error", Message=f"{str(e)}")

        try:
            createTable(dbname=__DEFAULT_DB_NAME__, tablename=__DEFAULT_DB_TABLE__, dbConfig=__DEFAULT_DB_CONFIG__)
            showGood(goodRule="DB updated", Message=f"{__DEFAULT_DB_NAME__} has been updated successfully")
        except Exception as e:
            showError(exceptionRule="DB error", Message=f"{str(e)}")

class createuser:
    def __init__(self):
        pass

    def createuser(self, serverConfig):
        from utils.dbConnections import appendData, getdbname, search
        from utils.showMessage import showGood, askForInput , coloredMessage, showError
        from config.db import __DEFAULT_DB_NAME__, __DEFAULT_DB_TABLE__, __DEFAULT_DB_CONFIG__

        from getpass import getpass
        from hashlib import sha256
        from os.path import exists

        if exists(getdbname(__DEFAULT_DB_NAME__)):
            FIRST_NAME = askForInput("First name: ")
            SECOND_NAME = askForInput("Second name: ")
            EMAIL = askForInput("Email: ")
            PHONE = askForInput("Phone: ")

            __DEFAULT_DB_USERNAME__ = askForInput("Username: ")
            if len(search(__DEFAULT_DB_NAME__, __DEFAULT_DB_TABLE__ , __DEFAULT_DB_CONFIG__, [None, None, __DEFAULT_DB_USERNAME__, None, None, None, None])) != 0:
                showError(exceptionRule="DB error", Message="The username you selected already exists")
                exit()

            DB_PASSWORD = getpass(coloredMessage('Password: ', 'blue'))
            DB_PASSWORD_AGAIN = getpass(coloredMessage('Password Confirmation: ', 'blue'))

            if DB_PASSWORD == DB_PASSWORD_AGAIN:
                pass
            else:
                showError(exceptionRule="Password Error", Message="The passwords you entered doesn't match")
                exit()

            PASSWORD_BYTES = DB_PASSWORD.encode('UTF-8')

            PASSWORD_HASH = sha256(PASSWORD_BYTES).hexdigest()
            PASSWORD_HASH = str(PASSWORD_HASH)

            appendData(dbname=__DEFAULT_DB_NAME__, tablename=__DEFAULT_DB_TABLE__, dbConfig=[FIRST_NAME, SECOND_NAME, __DEFAULT_DB_USERNAME__, PASSWORD_HASH, EMAIL, PHONE, None])
            showGood(goodRule="\nUser created", Message=f"{__DEFAULT_DB_USERNAME__} has been added into the database: {__DEFAULT_DB_NAME__}")
        else:
            showError(exceptionRule="Path Error", Message="The database hasn't been created, please run migrate to create it.")
