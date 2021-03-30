'''
this code has been taken from github.com/DEMON1A/VCS
that's owned by me. so i'm able to use it anywhere.
'''

from colorama import init
from termcolor import colored

def showError(exceptionRule , Message):
    init()

    ruleColored = colored(exceptionRule , 'yellow' , attrs=['bold'])
    messageColored = colored(Message , 'red' , attrs=['bold'])

    errorMessage = f"{ruleColored}: {messageColored}"
    print(errorMessage)

def showGood(goodRule , Message):
    init()

    ruleColored = colored(goodRule , 'yellow' , attrs=['bold'])
    messageColored = colored(Message , 'green' , attrs=['bold'])

    errorMessage = f"{ruleColored}: {messageColored}"
    print(errorMessage)

def askForInput(userMessage):
    init()

    messageColored = colored(userMessage, 'blue', attrs=['bold'])
    userInput = input(messageColored)

    return userInput