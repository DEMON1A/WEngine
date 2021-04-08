'''
this util has been created to read and write the logs
into it's path on the config/settings.py `LOGS_PATH` variable
helpting the server admin to know who's visiting his website
and idenify users visiting it.
'''

from config.settings import LOGS_PATH
from utils.showMessage import showError

from os.path import exists
from datetime import datetime

def readLogs():
    if exists(LOGS_PATH):
        fileContent = open(f"{LOGS_PATH}/server.log", 'r').read()
        return fileContent
    else:
        showError(exceptionRule="Paths Error", Message="WEngine couldn't find the LOGS_PATH, please double check it")


def writeLogs(clientIP, userAgent, endpointVisited, responseCode, requestMethod):
    if exists(LOGS_PATH):
        currentDate = datetime.now()
        dateString = f"{currentDate.year}/{currentDate.month}/{currentDate.day}"
        writtenMessage = f"[{dateString}] [{clientIP}] - [{userAgent}]: {requestMethod} {endpointVisited} - {responseCode}\n"

        with open(f"{LOGS_PATH}/server.log", 'a') as logsFile:
            logsFile.write(writtenMessage)
            logsFile.close()
    else:
        showError(exceptionRule="Paths Error", Message="WEngine couldn't find the LOGS_PATH, please double check it")

def cleanServerLogs():
    if exists(LOGS_PATH):
        with open(f"{LOGS_PATH}/server.log", 'w') as logsFile:
            logsFile.write('')
            logsFile.close()
        return True
    else:
        showError(exceptionRule="Paths Error", Message="WEngine couldn't find the LOGS_PATH, please double check it")
        return False
