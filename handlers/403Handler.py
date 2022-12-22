from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders, requestParameters):
    return returnRenderedTemplate("WEngine/defaultPages/403.html", {}, 403)