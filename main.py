import optparse
import concurrent.futures

from modes.classes import *
from utils.showMessage import showError


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
    optionsParser.add_option("--mode", "-m", default="runserver", dest="mode", help="The Mode That Contains The Actions You Wants To Perform")

    toolOptions,_ = optionsParser.parse_args()
    return toolOptions

def mainFunction(Options):
    '''
    the mode should be checked before everything. if there's no mood the tool should run the server
    but if there's a mode. it should check it. then use modules with it if modules is used
    but i's still on development process
    '''

    try:
        userMode = Options.mode

        modeClass = globals()[userMode]()
        modeFunction = getattr(modeClass , userMode)

        applicationConfig = buildConfig()
        modeFunction(applicationConfig)
    except Exception as e:
        showError(exceptionRule="Mode Error" , Message=f"The mode {userMode} doesn't exists on the classes")

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as optionsCollector:
        toolOptions = optionsCollector.submit(collectOptions)
        toolOptions = toolOptions.result()

    with concurrent.futures.ThreadPoolExecutor() as mainThreader:
        _ = mainThreader.submit(mainFunction , toolOptions)