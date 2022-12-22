import importlib
from utils.showMessage import showError

def callHandler(handlerName, requestHeaders, requestParameters):
    modulePath = f"handlers.{handlerName}".replace('.py' , '')
    handlerFunction = importlib.import_module(modulePath)
    responseContent, responseHeaders, responseCode = handlerFunction.Handler(requestHeaders, requestParameters)

    if type(responseContent) != str:
        showError(exceptionRule="Handler Error", Message=f"The response content the {handlerName} is returning, isn't a valid string")
        exit()

    if type(responseHeaders) != dict:
        showError(exceptionRule="Handler Error", Message=f"The response headers the {handlerName} is returning, isn't a valid dict")
        exit()

    if type(responseCode) != int:
        showError(exceptionRule="Handler Error", Message=f"The response code the {handlerName} is returning, isn't a valid integar")
        exit()

    try:
        _ = responseHeaders['content-type']
    except Exception:
        responseHeaders['content-type'] = "text/html"

    return responseContent, responseHeaders, responseCode
