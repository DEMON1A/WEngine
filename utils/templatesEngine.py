import re
from os.path import exists
from os import popen
from datetime import datetime
from urllib.parse import urlencode
from time import gmtime, strftime

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

    def url_to(self, templateSyntax, templateVariables={}):
        detectPattern = r"url\_to\((..*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionArguments = detectFunction.group()[6:][1:][:-1]
            if ":" in functionArguments:
                argumentsList = functionArguments.split(':')
                
                try:
                    firstArgument = argumentsList[0].replace('"', '').replace("'", '').strip()
                    secondArgument = argumentsList[1].replace('"', '').replace("'", '').strip()

                    try:
                        basePath = urlModes[firstArgument]
                        basePath += f"/{secondArgument}"
                    except Exception:
                        basePath = secondArgument
                except Exception:
                    basePath = firstArgument
            elif functionArguments == "" or functionArguments == " ":
                basePath = "/"
            else:
                basePath = functionArguments.replace('"', '').replace("'", '')
            basePath = basePath.replace('//', '/')
        else:
            basePath = ""

        return basePath

    def exec(self, templateSyntax, templateVariables={}):
        if ALLOW_TEMPLATE_EXEC:
            detectPattern = r"exec\((.*|)\)"

            detectFunction = re.search(detectPattern, templateSyntax)
            if detectFunction != None:
                functionsArgument = detectFunction.group()[4:][1:][:-1]
                functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
                exec(functionsArgument)
                return ""
        else:
            return ""

    def system(self, templateSyntax, templateVariables={}):
        if ALLLOW_TEMPLATE_SYSTEM:
            detectPattern = r"system\((.*|)\)"

            detectFunction = re.search(detectPattern, templateSyntax)
            if detectFunction != None:
                functionsArgument = detectFunction.group()[6:][1:][:-1]
                functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
                
                cmdResults = popen(functionsArgument).read()
                return cmdResults
        else:
            return ""

    def removetags(self, templateSyntax, templateVariables={}):
        detectPattern = r"removetags\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[10:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = replaceString.replace('<', '').replace('>', '')
                return rString
            except Exception:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def removeqoutes(self, templateSyntax, templateVariables={}):
        detectPattern = r"removeqoutes\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[12:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = replaceString.replace('"', '').replace("'", '')
                return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def markdown(self, templateSyntax, templateVariables={}):
        detectPattern = r"markdown\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[8:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = createMarkdown(mdSyntax=replaceString)
                return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def securemarkdown(self, templateSyntax, templateVariables={}):
        detectPattern = r"securemarkdown\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[14:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = secureMarkdown(mdSyntax=replaceString)
                return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def readfile(self, templateSyntax, templateVariables={}):
        detectPattern = r"readfile\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[8:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = readFile(replaceString)

                if not rString: return ""
                else: return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def base64(self, templateSyntax, templateVariables={}):
        detectPattern = r"base64\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[6:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = base64Encode(encodeString=replaceString)

                if not rString: return ""
                else: return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def base32(self, templateSyntax, templateVariables={}):
        detectPattern = r"base32\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[6:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()
            
            try:
                replaceString = templateVariables[functionsArgument]
                rString = base32Encode(encodeString=replaceString)

                if not rString: return ""
                else: return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""

    def date(self, templateSyntax, templateVariables={}):
        detectPattern = r"date\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[4:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()

            currentDate = datetime.now()
            dateString = f"{currentDate.year}{functionsArgument}{currentDate.month}{functionsArgument}{currentDate.day}"

            return dateString
        else:
            return ""

    def time(self, templateSyntax, templateVariables={}):
        detectPattern = r"time\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[4:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()

            currentTime = strftime(f"%H{functionsArgument}%M{functionsArgument}%S", gmtime())
            return currentTime
        else:
            return ""

    def urlencode(self, templateSyntax, templateVariables={}):
        detectPattern = r"urlencode\((.*|)\)"

        detectFunction = re.search(detectPattern, templateSyntax)
        if detectFunction != None:
            functionsArgument = detectFunction.group()[9:][1:][:-1]
            functionsArgument = functionsArgument.replace('"', '').replace("'", '').strip()

            try:
                replaceString = templateVariables[functionsArgument]
                rString = urlencode(replaceString)

                if not rString: return ""
                else: return rString
            except Exception as e:
                showError(exceptionRule="Template Error", Message="You're using a template variable that doesn't exists")
                return ""
        else:
            return ""