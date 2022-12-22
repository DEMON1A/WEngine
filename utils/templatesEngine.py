import re
from os.path import exists
from os import popen
from datetime import datetime
from time import gmtime, strftime

from urllib.parse import quote
from urllib.parse import urlencode

from utils.showMessage import showError
from utils.markdownSupport import createMarkdown, secureMarkdown
from utils.fileReader import readFile
from utils.baseEncode import base64Encode, base32Encode

from config.urlsBase import urlModes
from config.settings import ALLOW_TEMPLATE_EXEC, ALLLOW_TEMPLATE_SYSTEM

class templatesParser:
    def __init__(self):
        pass

    def detectStrings(self, lineOfCode, templateVariables={}):
        detectPattern = r"\{\-.*\-\}\,"
        
        templateSyntaxDetected = re.search(detectPattern, lineOfCode)
        if templateSyntaxDetected != None:
            codeSyntax = templateSyntaxDetected.group()
            if "," not in codeSyntax:
                showError(exceptionRule="Template Error", Message="There's no comma's seprating your template syntax can result in parsing issues, please use ',' after every syntax")
                return False
            else:
                reSearch = re.search(r"\}.*\{", codeSyntax)
                
                if reSearch != None:
                    replaceString = reSearch.group()
                    codeSyntax = codeSyntax.replace(replaceString, '},{')

                tempList = codeSyntax.split(',')
                syntaxList = []
                duplicateList = []

                for singleItem in tempList:
                    singleItem = singleItem.strip()

                    if singleItem not in duplicateList and singleItem != '':
                        syntaxList.append(singleItem)

                    duplicateList.append(singleItem)

                return syntaxList
        else:
            return []

    def detectFunctions(self, lineOfCode, templateVariables={}):
        detectPattern = r"\{\{.*\}\}\,"
        
        templateSyntaxDetected = re.search(detectPattern, lineOfCode)
        if templateSyntaxDetected != None:
            codeSyntax = templateSyntaxDetected.group()
            if "," not in codeSyntax:
                showError(exceptionRule="Template Error", Message="There's no comma's seprating your template syntax can result in parsing issues, please use ',' after every syntax")
                return False
            else:
                tempList = codeSyntax.split(',')
                syntaxList = []
                duplicateList = []

                for singleItem in tempList:
                    singleItem = singleItem.strip()

                    if singleItem not in duplicateList and singleItem != '':
                        syntaxList.append(singleItem)

                    duplicateList.append(singleItem)

                return syntaxList
        else:
            return []

    def filterString(self, templateSyntax, functionName):
        fString = templateSyntax.replace(functionName, '')
        fString = fString.strip()

        return fString

    def detectFunction(self, templateSyntax):
        charactersList = []

        for singleCharacter in templateSyntax:
            if singleCharacter != "(":
                charactersList.append(singleCharacter)
            else:
                break

        functionName = ''.join(charactersList)
        return functionName
    
    def getArguments(self, templateSyntax, functionName):
        argumentString = templateSyntax[:-1][1:]
        argumentString = argumentString.strip()

        return argumentString

    def getQoutes(self, aString, detectionStr):
        stringList = []
        stringsList = []
        firstdStringFound = False

        for singleCharacter in aString:
            if singleCharacter == detectionStr:
                if firstdStringFound:
                    stringList.append(singleCharacter)
                    realString = ''.join(stringList)
                    stringsList.append(realString)

                    firstdStringFound = False
                    stringList = []
                else:
                    firstdStringFound = True
                    stringList.append(singleCharacter)
            elif firstdStringFound:
                stringList.append(singleCharacter)
            else:
                pass

        return stringsList

    def parseArguments(self, templateSyntax):
        globalCounter = 0
        argumentsMap = {}

        functionName = self.detectFunction(templateSyntax)
        templateSyntax = self.filterString(templateSyntax, functionName)

        argumentString = self.getArguments(templateSyntax, functionName)
        argumentsList = []

        argumentsList += self.getQoutes(argumentString, "'")
        argumentsList += self.getQoutes(argumentString, '"')

        for singleQoute in argumentsList:
            globalCounter += 1
            replaceString = f"arg{str(globalCounter)}"
            argumentsMap[replaceString] = singleQoute
            argumentString = argumentString.replace(singleQoute, replaceString)

        argumentsParameters = argumentString.split(':')
        fullValueParameters = []

        for singleParameter in argumentsParameters:
            singleParameter = singleParameter.strip()
            fullValueParameters.append(argumentsMap[singleParameter].replace('"', '').replace("'", ''))

        return fullValueParameters

    def detectMode(self, modeString):
        if modeString.lower() == "variable" or modeString.lower() == "var":
            return "variable"
        elif modeString.lower() == "global" or modeString.lower() == "glob":
            return "global"
        else:
            return "global"

    def url_to(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[2]]

                basePath = urlModes[syntaxArguments[1]]
                basePath += f"{variableValue}"
            except Exception:
                showError(exceptionRule="Mode or Variable error", Message="There's an error with the mode or the variable, check both of them.")
                return ""
        else:
            try:
                basePath = urlModes[syntaxArguments[0]]
                basePath += f"{syntaxArguments[1]}"
            except Exception:
                showError(exceptionRule="Mode error", Message="There's an error with your mode, double check it.")
                return ""

        basePath = basePath.replace('//', '/')
        return basePath

    def exec(self, templateSyntax, templateVariables={}):
        if ALLOW_TEMPLATE_EXEC:
            syntaxArguments = self.parseArguments(templateSyntax)
            Mode = self.detectMode(syntaxArguments[0])

            if Mode == "variable":
                try:
                    execValue = templateVariables[syntaxArguments[1]]
                    exec(execValue)
                    return ""
                except Exception:
                    showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined.")
                    return ""
            else:
                exec(syntaxArguments[1])
                return ""
        else:
            return ""

    def system(self, templateSyntax, templateVariables={}):
        if ALLLOW_TEMPLATE_SYSTEM:
            syntaxArguments = self.parseArguments(templateSyntax)
            Mode = self.detectMode(syntaxArguments[0])

            if Mode == "variable":
                try:
                    execValue = templateVariables[syntaxArguments[1]]
                    cmdResults = popen(execValue).read()
                    return cmdResults
                except Exception:
                    showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                    return ""
            else:
                cmdResults = popen(syntaxArguments[1]).read()
                return cmdResults
        else:
            return ""

    def removetags(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = variableValue.replace('<', '').replace('>', '')
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = replaceString.replace('<', '').replace('>', '')
            return replaceString

    def removeqoutes(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = variableValue.replace('"', '').replace("'", '')
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = replaceString.replace('"', '').replace("'", '')
            return replaceString

    def markdown(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = createMarkdown(mdSyntax=variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = createMarkdown(mdSyntax=replaceString)
            return replaceString

    def securemarkdown(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = secureMarkdown(mdSyntax=variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = secureMarkdown(mdSyntax=replaceString)
            return replaceString

    def readfile(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = readFile(variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = readFile(replaceString)
            return replaceString

    def base64(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = base64Encode(variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = base64Encode(replaceString)
            return replaceString

    def base32(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = base32Encode(variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = base32Encode(replaceString)
            return replaceString

    def date(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        currentDate = datetime.now()
        dateString = f"{currentDate.year},{currentDate.month},{currentDate.day}"

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = dateString.replace(',', variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = dateString.replace(',', replaceString)
            return replaceString

    def time(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        currentTime = strftime(f"%H,%M,%S", gmtime())
        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = currentTime.replace(',', variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = currentTime.replace(',', replaceString)
            return replaceString

    def urlencode(self, templateSyntax, templateVariables={}):
        syntaxArguments = self.parseArguments(templateSyntax)
        Mode = self.detectMode(syntaxArguments[0])

        if Mode == "variable":
            try:
                variableValue = templateVariables[syntaxArguments[1]]
                variableValue = quote(variableValue)
                return variableValue
            except Exception:
                showError(exceptionRule="Variables Error", Message="The variable you're using isn't defined")
                return ""
        else:
            replaceString = syntaxArguments[1]
            replaceString = urlencode(replaceString)
            return replaceString
