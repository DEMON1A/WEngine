from utils.makeResponse import returnRenderedTemplate
from utils.makeResponse import returnHTTPBasicResponse

def Handler(requestHeaders, requestParameters):
    return returnRenderedTemplate("WEngine/index.html", {}, 200)