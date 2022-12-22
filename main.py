import optparse
import concurrent.futures
import sys
import inspect

from modes.classes import *
from utils.showMessage import showError
from utils.showMessage import showGood


'''
import only used variables from settings. the security
part should be seprated from the build config function
and should be includes on the utils
'''

from config.settings import SERVER_DOMAIN
from config.settings import SERVER_EMAIL
from config.settings import SERVER_PORT
from config.settings import LOGS_PATH
from config.settings import TEMPLATES_PATH
from config.settings import STATIC_PATH
from config.settings import STATIC_PATH
from config.settings import TMP_PATH
from config.settings import DEFAULT_DOCUMENT

def buildConfig():
    mainConfig = {}

    mainConfig['SERVER_PORT'] = SERVER_PORT
    mainConfig['SERVER_EMAIL'] = SERVER_EMAIL
    mainConfig['SERVER_DOMAIN'] = SERVER_DOMAIN

    mainConfig['LOGS_PATH'] = LOGS_PATH
    mainConfig['TEMPLATES_PATH'] = TEMPLATES_PATH
    mainConfig['STATIC_PATH'] = STATIC_PATH
    mainConfig['TMP_PATH'] = TMP_PATH
    mainConfig['DEFAULT_DOCUMENT'] = DEFAULT_DOCUMENT

    return mainConfig

def collectOptions():
    optionsParser = optparse.OptionParser()
    optionsParser.add_option("--mode", "-m", default="runserver", dest="mode", help="The mode that contains the actions you wants to execute")
    optionsParser.add_option("--list", "-l", action="store_true", dest="list", help="List all the available modes you can use")

    toolOptions,_ = optionsParser.parse_args()
    return toolOptions

def mainFunction(Options):
    '''
    the mode should be checked before everything. if there's no mood the tool should run the server
    but if there's a mode. it should check it. then use modules with it if modules is used
    but i's still on development process
    '''

    if Options.list == None:
        try:
            userMode = Options.mode

            modeClass = globals()[userMode]()
            modeFunction = getattr(modeClass , userMode)

            applicationConfig = buildConfig()
            modeFunction(applicationConfig)
        except Exception as e:
            showError(exceptionRule="Mode Error", Message=f"The mode {userMode} doesn't exists on the classes")
    else:
        try:
            from modes import classes
            moduleName = sys.modules[classes.__name__]

            for _, classObject in inspect.getmembers(moduleName):
                if inspect.isclass(classObject):
                    showGood(goodRule=classObject.__name__, Message=classObject().description)
        except Exception as e:
            showError(exceptionRule="List error", Message="We couldn't list the program modes")

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as optionsCollector:
        toolOptions = optionsCollector.submit(collectOptions)
        toolOptions = toolOptions.result()

    with concurrent.futures.ThreadPoolExecutor() as mainThreader:
        _ = mainThreader.submit(mainFunction , toolOptions)