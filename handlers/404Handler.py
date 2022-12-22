from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders, requestParameters):
    return returnRenderedTemplate("WEngine/defaultPages/404.html", {}, 404)