'''
this's a basic util for the server handlers. it's easy
to use and works fine with the server. all it does is formating
the user input and adding default values to make it easier
to the user to use it. otherwise. the user have to return his
own arguments.

this function also includes a template parser that returns a hall templates
with the program template engine
'''
from config.settings import TEMPLATES_PATH
from config.templatesFunctions import __FUNCTIONS__
from urllib.parse import quote

from utils.fileReader import readFile, readFileByLines
from utils.templatesEngine import templatesParser
from utils.showMessage import showError

detectedStrings = []
detectedFunctions = []
replacedFileContent = ""

def returnHTTPBasicResponse(responseText, responseHeaders={}, responseCode=200):
    return responseText, responseHeaders, responseCode

def returnBasicFileContent(filePath, responseHeaders={}, responseCode=200):
    filePath = f"{TEMPLATES_PATH}/{filePath}"
    requestFileContent = readFile(filePath)

    if not requestFileContent: return '500 Internal Server Error', {}, 500
    else: return requestFileContent, responseHeaders, responseCode

def returnRenderedTemplate(filePath, responseHeaders={}, responseCode=200, templateVariables={}):
    global detectedStrings, detectedFunctions, replacedFileContent

    filePath = f"{TEMPLATES_PATH}/{filePath}"
    requestFileContent = readFileByLines(filePath)
    realFileContent = readFile(filePath)

    if not requestFileContent:
        return '500 Internal Server Error', {}, 500
    else:
        Parser = templatesParser()
        for singleLine in requestFileContent:
            detectedStrings += Parser.detectStrings(lineOfCode=singleLine)
            detectedFunctions += Parser.detectFunctions(lineOfCode=singleLine)

        if len(detectedStrings) != 0:
            for dString in detectedStrings:
                dRealString = dString[2:][:-2].strip()

                try:
                    userString = templateVariables[dRealString]
                    replacedFileContent = realFileContent.replace(f"{dString},", str(userString))
                    realFileContent = replacedFileContent
                except Exception:
                    showError(exceptionRule="Template Error", Message=f"You're using an undefined variable '{dRealString}' on your template")
                    exit()

        if len(detectedFunctions) != 0:
            for dFunction in detectedFunctions:
                dRealFunction = dFunction[2:][:-2].strip()
                charactersList = []

                for singleCharacter in dRealFunction:
                    if singleCharacter != "(":
                        charactersList.append(singleCharacter)
                    else:
                        break

                functionName = ''.join(charactersList)

                if functionName in __FUNCTIONS__:
                    parserFunction = getattr(Parser, functionName)
                    responseContent = parserFunction(dRealFunction, templateVariables)

                    replacedFileContent = realFileContent.replace(f"{dFunction},", responseContent)
                    realFileContent = replacedFileContent
                else:
                    showError(exceptionRule="Template Error", Message=f"You're using a template function '{dRealFunction}' that doesn't exists")
                    exit()

    return replacedFileContent, responseHeaders, responseCode

def createNewCookie(cookieName, cookieValue, cookiePath="/", maxAge=86400):
    # cookieName = str
    # cookieValue = str
    # maxAge = int
    # domainName = str

    # security protection, pervent escaping cookies options.
    # with full support to `;` character
    cookieValue = quote(cookieValue)

    # security protection, to avoid some but not all cookie bombing attacks
    # limit the max cookie value into: 255 characters
    if len(cookieValue) > 255:
        cookieValue = "empty"
    else:
        cookieValue = cookieValue

    # cookiename validtion. because it could be used for some attacks too.
    # `;` character isn't important on the cookiename. it will be stripped from the string
    cookieName = cookieName.replace(';', '')

    if len(cookieName) > 255:
        cookieName = "empty"
    else:
        cookieName = cookieName

    # path is imported over there. it can't impact that much but more layers
    # of protection is better. gonna encode the path
    cookiePath = quote(cookiePath)

    # cover encoded values with double qoutes.
    if "%" in cookieValue:
        cookieValue = f'"{cookieValue}"'

    if "%" in cookiePath:
        cookiePath = f'"{cookiePath}"'

    headerName = str("Set-Cookie")
    headerValue = str(f"{cookieName}={cookieValue}; Max-Age={str(maxAge)}; Path={cookiePath}; Secure; HttpOnly")
    headerValue = headerValue.replace('\n', '').replace('\r', '')

    headerDict = {
        headerName: headerValue
    }

    return headerDict

def deleteCookie(cookieName):
    cookieName = cookieName.replace(';', '')

    if len(cookieName) > 255:
        cookieName = "empty"
    else:
        cookieName = cookieName

    headerName = str("Set-Cookie")
    headerValue = str(f"{cookieName}=deleted; Max-Age=0; Secure; HttpOnly")

    headerDict = {
        headerName: headerValue
    }

    return headerDict
