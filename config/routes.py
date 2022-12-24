import json
import os 

def createRoute(routeName, routePath):
    CONFIG_PATH = os.path.join(os.getcwd(), 'config\\routes.json')
    newRoute = { routeName: routePath }
    currentRoutes = loadRoutes()
    currentRoutes.update(newRoute)

    with open(CONFIG_PATH, 'w') as routesFile:
        json.dump(currentRoutes, routesFile, sort_keys=True, indent=4)

    # Create the handler file
    HANDLER_PATH = os.path.join(os.getcwd(), f'handlers\\{routePath}')

    HANDLER_FILE = """from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders, requestParameters):
    return returnRenderedTemplate("WEngine/index.html", {}, 200)
    """

    if os.path.exists(HANDLER_PATH):
        # A handler with that name already exists
        from utils.showMessage import showError
        from utils.showMessage import showGood

        showError(exceptionRule="Note", Message="There's a handler with that name already")
        userAgree = input("Would you like to replace it with a fresh one? [Y] or would you like to use the same handler for the new route? [K]: ")
        if userAgree.upper() == "Y":
            with open(HANDLER_PATH, 'w') as handlerFile:
                handlerFile.write(HANDLER_FILE)
                handlerFile.close()
            
            showGood(goodRule="File replaced", Message="We have sucessfully replaced the current handler")
        elif userAgree.upper() == "K":
            # Do nothing to the file, literally
            pass
        else:
            # Keep the route by default, that's the safe option
            pass
    else:
        with open(HANDLER_PATH, "w") as handlerFile:
            handlerFile.write(HANDLER_FILE)
            handlerFile.close()

def loadRoutes():
    CONFIG_PATH = os.path.join(os.getcwd(), 'config\\routes.json')
    jsonContent = open(CONFIG_PATH, 'r').read()
    return json.loads(jsonContent)