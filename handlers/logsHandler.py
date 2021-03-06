from utils.makeResponse import returnHTTPBasicResponse, returnRenderedTemplate
from utils.logsController import readLogs
from config.settings import PUBLIC_LOGS

def Handler(responseHeaders):
    if PUBLIC_LOGS:
        return returnHTTPBasicResponse(readLogs(), {"content-type":"text/plain"}, 200)
    else:
        return returnRenderedTemplate('WEngine/defaultPages/403.html', {}, 403)
