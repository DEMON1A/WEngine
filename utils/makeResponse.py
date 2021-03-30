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