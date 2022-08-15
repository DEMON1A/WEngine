'''
this function is used only to read HTML files the server is using
and return it's content UTF-8 encoded to the server so it can serve
it

this function also includes an LFI protection to avoid accessing files
outside the templates folder. and that's the only folder you're
allowed to access files from this function only

if you need to read a file on your handler. please use this function.
this function has been created with a security protections to disallow
external attacks. if you gonna use an external function. then it's
not WEngine fault.
'''
from utils.showMessage import showError
from os.path import isdir, islink
from config.settings import ALLOW_SYMLINKS

def readFile(filePath):
    try:
        filePath = filePath.replace('..', '')

        if not ALLOW_SYMLINKS:
            if islink(filePath):
                showError(exceptionRule="File Error", Message="Symlink is disabled while the user is trying to read a symlink file")
                return False
            else:
                fileContent = open(filePath, 'r')
                fileContent = fileContent.read()
                return fileContent
        else:
            fileContent = open(filePath, 'r')
            fileContent = fileContent.read()
            return fileContent
    except Exception:
        if isdir(filePath):
            return True
        else:
            showError(exceptionRule="File Error", Message=f"There's an error trying to open {filePath}")
            return False

def readFileByLines(filePath):
    try:
        filePath = filePath.replace('..', '')

        if not ALLOW_SYMLINKS:
            if islink(filePath):
                showError(exceptionRule="File Error", Message="Symlink is disabled while the user is trying to read a symlink file")
                return False
            else:
                fileContent = open(filePath, 'r')
                fileContent = fileContent.readlines()
                return fileContent
        else:
            fileContent = open(filePath, 'r')
            fileContent = fileContent.readlines()
            return fileContent
    except Exception:
        if isdir(filePath):
            return True
        else:
            showError(exceptionRule="File Error", Message=f"There's an error trying to open {filePath}")
            return False
