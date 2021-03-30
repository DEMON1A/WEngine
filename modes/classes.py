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
        pass